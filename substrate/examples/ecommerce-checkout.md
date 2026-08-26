# Ecommerce Checkout

This example shows ecommerce checkout as a core Substrate subject. It uses the
same 9 primitives as the other examples and does not require an implementation
design.

## Graph

The graph contains checkout entities and their dependencies:

```text
customer:c0 -> cart:cart0
cart:cart0  -> sku:sku0
cart:cart0  -> sku:sku1
sku:sku0    -> inventory:inv0
cart:cart0  -> payment:pay0
cart:cart0  -> order:ord0
order:ord0  -> shipment:ship0
order:ord0  -> notification:notif0
```

Edges represent checkout dependency: a cart depends on customer context, SKUs,
inventory availability, payment authorization, order creation, shipment, and
notification.

## Typed field

The subject uses typed fields for checkout state:

- cart status;
- item quantity;
- price;
- inventory availability;
- payment risk;
- payment status;
- order status;
- shipment status;
- notification status.

## Placement

Fields are placed on the graph where they have domain meaning:

- item quantity is placed on cart-to-SKU edges;
- price is placed on SKU nodes or cart item edges;
- inventory availability is placed on inventory nodes;
- payment risk and payment status are placed on payment nodes;
- cart status is placed on cart nodes;
- order status is placed on order nodes;
- shipment status is placed on shipment nodes;
- notification status is placed on notification nodes.

## State

The current state is the observed checkout condition:

```text
cart:cart0 status: submitted
cart:cart0 -> sku:sku0 quantity: 1 price: 40
cart:cart0 -> sku:sku1 quantity: 2 price: 25
inventory:inv0 availability: available
payment:pay0 risk: low
payment:pay0 status: not_authorized
order:ord0 status: not_created
shipment:ship0 status: not_arranged
notification:notif0 status: not_sent
```

## Action

Prefer a valid checkout path that creates an order while preserving payment
safety, inventory safety, and customer-visible correctness.

## Constraint

The checkout subject has hard validity rules:

- cannot create an order without a valid cart;
- cannot use unavailable inventory;
- cannot proceed when payment is blocked;
- cannot send notification before the order exists;
- cannot declare success when order status is not created.

## Evolution

Checkout state moves through allowed status changes:

```text
submitted
  -> priced
  -> inventory_available
  -> payment_authorized
  -> order_created
  -> shipment_arranged
  -> notification_sent
```

If a constraint fails, the state moves to a rejected, deferred, review, or failed
checkout state.

## Readout

The readout is the checkout decision:

```text
complete
reject
review
defer
failed_with_reason
```

The readout should include the customer-visible status and the reason when the
checkout does not complete.

## Validation

Validation checks that:

- every output follows from declared graph state;
- all constraint rules hold;
- hidden service state is not treated as observed state;
- customer-visible status matches declared checkout state;
- a successful checkout has created order status and valid payment and inventory
  status.

The purpose is not to build an ecommerce platform. The purpose is to show how
graph, typed field, placement, state, action, constraint, evolution, readout,
and validation can describe checkout as a Substrate subject.
