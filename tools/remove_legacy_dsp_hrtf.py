from pathlib import Path

path = Path('/home/ubuntu/frostsoulx/app/src/main/kotlin/dev/vxs/frostsoulx/ui/player/frostsoul/FrostSoulPlayer.kt')
text = path.read_text()

# Remove all DSP/HRTF state, parameter application, and dialog branches from FSPlayerControls.
start = text.index('    var dspMenuOpen by remember { mutableStateOf(false) }')
end = text.index('    Column(\n', start)
text = text[:start] + text[end:]

# Remove the remaining DSP/HRTF dialog branches from the utility row block.
branch_start = text.index('        if (dspMenuOpen) {')
branch_end = text.index('        FSSeekbar(\n', branch_start)
text = text[:branch_start] + text[branch_end:]

# Remove the wave/DSP button from the utility row.
wave_call = '''            FSDspMicButton(\n                active = dspEnabled,\n                onClick = { dspMenuOpen = true },\n                immersive = immersive,\n            )\n'''
if wave_call not in text:
    raise SystemExit('wave button call not found')
text = text.replace(wave_call, '', 1)

# Remove the legacy wave button, DSP menu, HRTF scan flow, and DSP slider helpers.
start = text.index('@Composable\nprivate fun FSDspMicButton(')
end = text.index('@Composable\nprivate fun FSDownloadButton(', start)
text = text[:start] + text[end:]

path.write_text(text)
print('Removed legacy DSP/HRTF player state, dialogs, helpers, and wave control.')
