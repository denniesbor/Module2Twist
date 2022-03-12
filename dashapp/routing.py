from channels.routing import ProtocolTypeRouter, URLRouter


application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    # "http": django_asgi_app,

    # # WebSocket chat handler
    # "websocket": AuthMiddlewareStack(
    #     URLRouter([
    #         url(r"^chat/admin/$", AdminChatConsumer.as_asgi()),
    #         url(r"^chat/$", PublicChatConsumer.as_asgi()),
    #     ])
    # ),
})