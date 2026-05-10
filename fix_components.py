import re

with open("client/src/components/advanced-filter-panel.tsx", "r") as f:
    content = f.read()

content = content.replace("@components/ui", "@/components/ui")

with open("client/src/components/advanced-filter-panel.tsx", "w") as f:
    f.write(content)

with open("client/src/components/ai-analysis-panel.tsx", "r") as f:
    content = f.read()

content = content.replace("@/hooks/use-toast", "@/hooks/use-toast") # Just in case

with open("client/src/components/ai-analysis-panel.tsx", "w") as f:
    f.write(content)

with open("client/src/components/email-list.tsx", "r") as f:
    content = f.read()

# Fix the map property issue
content = content.replace("email.labels.map", "(Array.isArray(email.labels) ? email.labels : []).map")

with open("client/src/components/email-list.tsx", "w") as f:
    f.write(content)
