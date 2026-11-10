# Fixtures

All fixtures are inline.

The cellular sheaf tests use:

- `cycle_sheaf(dimension, twisted=False)`: three nodes, identity restrictions;
- `cycle_sheaf(dimension, twisted=True)`: one restriction negated;
- `shared_coordinate_sheaf()`: two views that overlap on one coordinate.

The view record tests use inline keyed views for:

- agreeing overlap values;
- conflicting overlap values;
- counterfactual status preservation;
- support mismatch rejection.
