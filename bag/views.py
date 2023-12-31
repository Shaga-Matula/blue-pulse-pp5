from django.contrib import messages
from django.shortcuts import (
    HttpResponse,
    get_object_or_404,
    redirect,
    render,
    reverse,
)
from django.views import View

from merchandise.models import MerchandiseMod


def view_bag(request):
    """A view that renders the bag contents page"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    product = MerchandiseMod.objects.get(pk=item_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    size = None

    if "product_size" in request.POST:
        size = request.POST["product_size"]

    bag = request.session.get("bag", {})

    if size:
        if item_id in bag:
            items_by_size = bag[item_id]["items_by_size"]
            if size in items_by_size:
                items_by_size[size] += quantity
                msg = (
                    f"Updated size {size.upper()} {product.name} "
                    f"quantity to {items_by_size[size]}"
                )
                messages.success(request, msg)
            else:
                items_by_size[size] = quantity
                msg = f"Added size {size.upper()} ' \
                    {product.name} to your bag"
                messages.success(request, msg)

        else:
            bag[item_id] = {"items_by_size": {size: quantity}}
            messages.success(
                request,
                f"Added size {size.upper()} ' \
                    {product.name} to your bag",
            )
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(
                request, f"Updated {product.name} quantity to {bag[item_id]}"
            )

        else:
            bag[item_id] = quantity
            messages.success(request, f"Added {product.name} to your bag")

    request.session["bag"] = bag
    return redirect(redirect_url)


class AdjustBagView(View):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    def post(self, request, item_id):
        product = get_object_or_404(MerchandiseMod, pk=item_id)
        quantity = int(request.POST.get("quantity"))
        size = None
        if "product_size" in request.POST:
            size = request.POST["product_size"]
        bag = request.session.get("bag", {})

        if size:
            if quantity > 0:
                if item_id in bag:
                    bag[item_id]["items_by_size"][size] = quantity
                    messages.success(
                        request,
                        (
                            f"Updated size {size.upper()} ' \
                            {product.name} quantity to "
                            f'{bag[item_id]["items_by_size"][size]}'
                        ),
                    )
                else:
                    bag[item_id] = {"items_by_size": {size: quantity}}
                    messages.success(
                        request,
                        f"Removed size {size.upper()} ' \
                            {product.name} from your bag",
                    )
            else:
                if item_id in bag and size in bag[item_id]["items_by_size"]:
                    del bag[item_id]["items_by_size"][size]
                    if not bag[item_id]["items_by_size"]:
                        bag.pop(item_id)
                    messages.success(
                        request, f"Updated {product.name} quantity to ' \
                            {bag[item_id]}"
                    )
        else:
            if quantity > 0:
                bag[item_id] = quantity
                messages.success(
                    request, f"Updated {product.name} quantity to ' \
                        {bag[item_id]}"
                )
            else:
                bag.pop(item_id)
                messages.success(request, f"Removed ' \
                    {product.name} from your bag")

        request.session["bag"] = bag
        return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(MerchandiseMod, pk=item_id)
        size = None
        if "product_size" in request.POST:
            size = request.POST["product_size"]
        bag = request.session.get("bag", {})

        if size:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            messages.success(
                request, f"Removed size {size.upper()} ' \
                    {product.name} from your bag"
            )
        else:
            bag.pop(item_id)

        request.session["bag"] = bag
        return HttpResponse(status=200)
        messages.success(request, f"Removed {product.name} from your bag")

    except Exception as e:
        return HttpResponse(status=500)
