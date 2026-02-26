# Publishing (Windows + GitHub)

## Prereqs

- GitHub CLI installed and authenticated
- Repo initialized with commit history

## If `gh` is not in PATH

Use:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

## Create/push repo

```powershell
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin master
git push origin <tag>
```

## Create release with artifact

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" release create <tag> "dist/memory-context-pipeline.skill" --title "Memory Context Pipeline <tag>" --notes-file "docs/RELEASE_NOTES_<tag>.md"
```
