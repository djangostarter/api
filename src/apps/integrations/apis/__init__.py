from ninja import Router

from .third_party import router as third_party_router

router = Router(tags=["integrations"])

router.add_router("third-party", third_party_router)

