# Sensor Ingestion Framework

## Purpose

Use this framework when raw observations need to become bounded frames, views,
features, and processor-ready records.

## Reusable Concept

Adapters read sensor or stream data. Converters normalize it into frames.
Preprocessors build bounded views. Lenses and processors consume those views
without owning source truth.

## Uses CGF Pieces

- adapters;
- typed views;
- lenses;
- source refs;
- trace records;
- processor routing;
- failure records.

## Example Applications

- robots;
- IoT systems;
- simulations;
- industrial monitoring;
- health devices;
- environment sensing.

## When To Use

- Raw input is noisy, high-volume, streamed, or device-specific.
- Processing should not depend on hidden adapter state.
- Missing, delayed, low-quality, or malformed observations must be visible.
- Several processors need different views over the same source frame.

## When Not To Use

- Input is already a clean declared state.
- There is no source or device boundary.
- The project does not need traceable preprocessing.

## Boundary

Sensor ingestion creates views and records. It does not commit actions,
diagnoses, findings, or final application truth.

## Implementation Posture

Implementation should begin with synthetic or fixture streams and explicit
failure states before integrating real devices.
