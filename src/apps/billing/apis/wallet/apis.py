from ninja.router import Router
from ninja.errors import HttpError

from infra.auth import JwtBearer

from apps.billing.services import get_or_create_wallet, get_current_subscription
from .schemas import BalanceOut, WalletOut, CurrentSubscriptionOut


router = Router(tags=['wallet'])


@router.get('/balance', auth=JwtBearer(), response=BalanceOut, url_name='billing/wallet/balance')
def balance(request):
    user = request.auth
    if not user or not getattr(user, "is_authenticated", False):
        raise HttpError(401, '未登录或用户不存在！')

    wallet = get_or_create_wallet(user_id=user.id, currency='CNY')
    subscription = get_current_subscription(user_id=user.id)

    subscription_out = None
    if subscription:
        subscription_out = CurrentSubscriptionOut(
            id=subscription.id,
            plan_code=subscription.plan.code,
            plan_name=subscription.plan.name,
            status=subscription.status,
            current_period_end=subscription.current_period_end.isoformat() if subscription.current_period_end else None,
        )

    return BalanceOut(
        wallet=WalletOut(id=wallet.id, currency=wallet.currency, balance=wallet.balance),
        subscription=subscription_out,
    )
