# Industrial Robot Arm Graph Claim Boundary

This app demonstrates a CGF robot-control contract:

```text
explicit topology
bounded action candidate
safety gate
traceable emitted command
evidence path
```

It does not claim:

- real robot safety;
- certified ABB controller behavior;
- production manufacturing readiness;
- collision-free planning;
- force, torque, or thermal safety;
- autonomous task performance;
- benchmark performance;
- replacement of robotics engineers, safety systems, or vendor controllers.

The shipped Webots app is local-only. It can show that a simulator controller
can be placed behind CGF trace and safety-gate boundaries, but it is not a real
robot or production claim.
