from pathlib import Path

path = Path('/home/ubuntu/frostsoulx/app/src/main/kotlin/dev/vxs/frostsoulx/ui/player/frostsoul/FrostSoulPlayer.kt')
text = path.read_text()
start_marker = '        if (dspMenuOpen) {\n'
end_marker = '        FSSeekbar(\n'
if start_marker not in text:
    raise SystemExit('remaining DSP menu branch not found')
start = text.index(start_marker)
end = text.index(end_marker, start)
path.write_text(text[:start] + text[end:])
print('Removed remaining DSP/HRTF menu and scan branches.')
