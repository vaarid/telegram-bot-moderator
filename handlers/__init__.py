from .moderation import router as moderation_router
 
def setup_handlers(dp):
    dp.include_router(moderation_router) 