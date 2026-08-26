# Ecommerce Runtime Path

## Purpose

This example shows an ecommerce workflow as an Architecture path around a
declared checkout Substrate subject.

## Runtime Shape

```text
cart submitted -> checkout view -> inventory/payment/shipping proposals
  -> verification -> checkout commit -> service execution
  -> trace -> outcome -> value memory
```

## Architecture Responsibilities

- Event log records cart submission and service responses.
- Runtime graph view connects cart, inventory, payment, order, shipment, and
  notification roles.
- Services emit proposals, not final authority.
- Verification checks state freshness, policy, risk, and evidence.
- Commit chooses complete, review, defer, reject, or fail.
- Trace records accepted and rejected paths.
- Outcomes update future ranking, inhibition, or uncertainty.

## Safety Rules

- Inventory, payment, order creation, shipment, refund, and customer
  notification are commit-sensitive.
- Stale proposals must be rejected or revalidated.
- Outcome memory cannot override source-of-truth service state.
- Compensation paths must be traceable.

## Validation Questions

```text
1. What service state version did each proposal depend on?
2. Which proposal was committed?
3. Which rejected proposals remain counterfactual evidence?
4. What service outcome resolved the commit?
5. What value or inhibition update is allowed?
```
