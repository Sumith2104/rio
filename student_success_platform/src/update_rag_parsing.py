with open("js/app.js", "r", encoding="utf-8") as f:
    text = f.read()

target = """    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    aiText.innerHTML = data.ai_pedagogical_guidance.replace(/\\n\\n/g, '<br><br>').replace(/\\n/g, '<br>');

    if (data.prerequisite_concepts && data.prerequisite_concepts.length > 0) {
      prereqContainer.style.display = 'block';
      prereqPath.innerHTML = data.prerequisite_concepts.map((concept, idx) => {
        const arrow = idx < data.prerequisite_concepts.length - 1 ? `<span class="prereq-dag-arrow">&rarr;</span>` : '';
        return `<span class="prereq-dag-step">${concept}</span>${arrow}`;
      }).join(' ');
    } else {
      prereqContainer.style.display = 'none';
    }

    if (data.retrieved_material_chunks && data.retrieved_material_chunks.length > 0) {
      chunksList.innerHTML = data.retrieved_material_chunks.map(chunk => `
        <div class="rag-chunk-card">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <strong style="color:#000000;">${chunk.title} [${chunk.category}]</strong>
            <span style="font-family:monospace; font-size:0.72rem; color:#6B7280;">Dist: ${chunk.similarity_distance}</span>
          </div>
          <div style="line-height:1.4;">${chunk.chunk_excerpt}</div>
        </div>
      `).join('');
    } else {
      chunksList.innerHTML = `<div style="font-size:0.8rem; color:#6B7280;">No direct chunk matches found for this course.</div>`;
    }"""

replacement = """    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const resObj = data.result || data;
    const answer = resObj.scaffolded_answer || resObj.ai_pedagogical_guidance || 'No explanation generated.';
    const prereqs = resObj.prerequisite_ancestors || resObj.prerequisite_concepts || [];
    const sources = resObj.retrieved_sources || resObj.retrieved_material_chunks || [];

    aiText.innerHTML = answer.replace(/\\n\\n/g, '<br><br>').replace(/\\n/g, '<br>');

    if (prereqs && prereqs.length > 0) {
      prereqContainer.style.display = 'block';
      prereqPath.innerHTML = prereqs.map((concept, idx) => {
        const arrow = idx < prereqs.length - 1 ? `<span class="prereq-dag-arrow">&rarr;</span>` : '';
        return `<span class="prereq-dag-step">${concept}</span>${arrow}`;
      }).join(' ');
    } else {
      prereqContainer.style.display = 'none';
    }

    if (sources && sources.length > 0) {
      chunksList.innerHTML = sources.map(chunk => `
        <div class="rag-chunk-card">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <strong style="color:#000000;">${chunk.title} [${chunk.unit || chunk.category || 'Course Material'}]</strong>
            <span style="font-family:monospace; font-size:0.72rem; color:#6B7280;">Concept: ${chunk.concept || 'AIML-401'}</span>
          </div>
          <div style="line-height:1.4;">${chunk.chunk_excerpt || chunk.title + ' indexed for cognitive diagnosis.'}</div>
        </div>
      `).join('');
    } else {
      chunksList.innerHTML = `<div style="font-size:0.8rem; color:#6B7280;">No direct chunk matches found for this course.</div>`;
    }"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open("js/app.js", "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated submitSubjectRagQuery response parsing successfully.")
else:
    print("target not found")

