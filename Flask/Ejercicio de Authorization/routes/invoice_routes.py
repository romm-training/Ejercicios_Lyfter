from flask import Flask, jsonify, request, g

from dtos.invoice_dto import InvoiceCreateDTO, InvoiceDTO, InvoiceUpdateDTO
from services.invoice_service import InvoiceService
from routes.decorators import AuthenticationGuard
from roles import Role

_BASE_URL = "/api/v1/invoices"

def register_invoice_routes(
        app: Flask,
        invoice_service: InvoiceService,
        guard: AuthenticationGuard
) -> None:
    @app.route(f"{_BASE_URL}", methods=["GET"])
    @guard.require_authentication
    def get_all_invoices():
        args = request.args.to_dict()

        if g.current_user["role"] == Role.ADMIN:
            invoices = invoice_service.get_all()
        else:
            invoices = invoice_service.get_all_by_user_id(
                int(g.current_user["sub"])
                )
        return jsonify([i.model_dump(mode="json") for i in invoices])

    @app.route(f"{_BASE_URL}/<int:invoice_id>", methods=["GET"])
    @guard.require_authentication
    def get_invoice_id(invoice_id: int):
        if g.current_user["role"] == Role.ADMIN:
            user_id = None
        else:
            user_id = int(g.current_user["sub"])

        invoice = invoice_service.get_by_id(
            invoice_id,
            user_id
        )
        return jsonify(invoice.model_dump(mode="json")), 200

    @app.route(f"{_BASE_URL}", methods=["POST"])
    @guard.require_authentication
    def create_invoice():
        invoice_data = InvoiceCreateDTO.model_validate(request.json)
        created_invoice = invoice_service.create(
            int(g.current_user["sub"]),
            invoice_data
        )
        return jsonify(created_invoice.model_dump(mode="json")), 201


