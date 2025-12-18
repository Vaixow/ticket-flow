import csv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Ticket

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        error = "Credenciales inválidas."

    return render(request, "auth_login.html", {"error": error})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    qs = Ticket.objects.all().order_by("-creado_en")

    total = qs.count()
    nuevos = qs.filter(estado=Ticket.Estado.NUEVO).count()
    en_proceso = qs.filter(estado=Ticket.Estado.EN_PROCESO).count()
    resueltos = qs.filter(estado=Ticket.Estado.RESUELTO).count()

    por_prioridad = {
        "baja": qs.filter(prioridad=Ticket.Prioridad.BAJA).count(),
        "media": qs.filter(prioridad=Ticket.Prioridad.MEDIA).count(),
        "alta": qs.filter(prioridad=Ticket.Prioridad.ALTA).count(),
    }

    recientes = qs[:10]

    return render(request, "dashboard.html", {
        "total": total,
        "nuevos": nuevos,
        "en_proceso": en_proceso,
        "resueltos": resueltos,
        "por_prioridad": por_prioridad,
        "recientes": recientes,
        "now": timezone.now(),
    })

@login_required
def ticket_create(request):
    if request.method == "POST":
        Ticket.objects.create(
            titulo=request.POST.get("titulo", "").strip(),
            descripcion=request.POST.get("descripcion", "").strip(),
            categoria=request.POST.get("categoria", Ticket.Categoria.SOPORTE),
            prioridad=request.POST.get("prioridad", Ticket.Prioridad.MEDIA),
            estado=request.POST.get("estado", Ticket.Estado.NUEVO),
            creado_por=request.user,
        )
        return redirect("dashboard")

    return render(request, "ticket_form.html", {"mode": "create", "ticket": None, "Ticket": Ticket})

@login_required
def ticket_edit(request, pk: int):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        ticket.titulo = request.POST.get("titulo", "").strip()
        ticket.descripcion = request.POST.get("descripcion", "").strip()
        ticket.categoria = request.POST.get("categoria", ticket.categoria)
        ticket.prioridad = request.POST.get("prioridad", ticket.prioridad)
        ticket.estado = request.POST.get("estado", ticket.estado)
        ticket.save()
        return redirect("dashboard")

    return render(request, "ticket_form.html", {"mode": "edit", "ticket": ticket, "Ticket": Ticket})

@login_required
def ticket_delete(request, pk: int):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        ticket.delete()
        return redirect("dashboard")
    return redirect("dashboard")

@login_required
def export_csv(request):
    estado = (request.GET.get("estado") or "").strip()
    prioridad = (request.GET.get("prioridad") or "").strip()

    qs = Ticket.objects.select_related("creado_por").order_by("-creado_en")
    if estado:
        qs = qs.filter(estado=estado)
    if prioridad:
        qs = qs.filter(prioridad=prioridad)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="tickets_export.csv"'

    writer = csv.writer(response)
    writer.writerow(["id", "titulo", "estado", "prioridad", "categoria", "creado_por", "creado_en"])

    for t in qs:
        writer.writerow([t.id, t.titulo, t.estado, t.prioridad, t.categoria, t.creado_por.username, t.creado_en.isoformat()])

    return response
