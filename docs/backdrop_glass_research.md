# Backdrop glass implementation notes

## Official Compose graphics documentation

Source: https://developer.android.com/develop/ui/compose/graphics/draw/modifiers

Compose `GraphicsLayer` can record drawing commands with `rememberGraphicsLayer()` and `graphicsLayer.record { drawContent() }`, then replay the recorded layer with `drawLayer`. The same documentation describes `Modifier.graphicsLayer` as an offscreen rendering layer and notes that `RenderEffect` is applied to the layer.

## Official Compose image customization documentation

Source: https://developer.android.com/develop/ui/compose/graphics/images/customize

Compose supports clipping, borders, gradients, and image transformations through modifiers. These are supplementary surface treatments; they do not by themselves sample pixels behind a component.

## Dimezis BlurView reference

Source: https://github.com/Dimezis/BlurView

BlurView is a dynamic Android View blur library. Its documented 3.2.0 dependency is `com.github.Dimezis:BlurView:version-3.2.0`. The library uses a separate `BlurTarget` and `BlurView`, blurs underlying View content, and keeps BlurView children sharp. It uses a different API 31+ code path and requires the blur target not to contain the BlurView.

## Implementation decision

The app currently uses a single Compose hierarchy, so the safer scoped approach is a Compose `GraphicsLayer` recorder around the underlying NavHost and a sibling backdrop surface for the bottom navigation and mini-player. The surface replays the captured layer through Compose `BlurEffect` on Android 12+, with a fallback transparent material on older devices. Fine grain, low-opacity tint, edge border, upper highlight, and a small enlarged replay provide the requested material treatment without an opaque rectangle or a separate external dependency.
