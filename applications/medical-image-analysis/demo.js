const cases = window.CGF_MEDICAL_IMAGE_DEMO.cases;

const caseSelect = document.querySelector("#case-select");
const caseImage = document.querySelector("#case-image");
const caseTitle = document.querySelector("#case-title");
const caseSummary = document.querySelector("#case-summary");
const questionEl = document.querySelector("#case-question");
const reviewGoalEl = document.querySelector("#review-goal");
const decisionEl = document.querySelector("#decision");
const decisionMeaningEl = document.querySelector("#decision-meaning");
const reasonEl = document.querySelector("#reason");
const flowEl = document.querySelector("#flow");
const lensesEl = document.querySelector("#lenses");
const proposalsEl = document.querySelector("#proposals");
const rejectedEl = document.querySelector("#rejected");
const traceEl = document.querySelector("#trace");
const regionOverlay = document.querySelector("#region-overlay");

const lensLabels = {
  texture: "Texture lens",
  morphology: "Morphology lens",
  context: "Context lens",
};

const proposalLabels = {
  "texture-proposer": "Texture route",
  "morphology-proposer": "Morphology route",
  "combined-review-proposer": "Combined evidence route",
};

const featureLabels = {
  texture_contrast: "texture contrast",
  region_quality: "region quality",
  cell_density: "cell density",
  boundary_clarity: "boundary clarity",
  source_quality: "source quality",
  collection_flag: "source type",
};

const decisionText = {
  commit: "The graph found enough support to commit within this demo contract.",
  review: "The graph found a best-supported route, but it still requires review.",
  abstain: "No proposal had enough support, so the graph refuses to create authority.",
  defer: "The graph could not complete the analysis path and deferred the case.",
};

function formatNumber(value) {
  return typeof value === "number" ? value.toFixed(2) : String(value);
}

function readableFeature(key, value) {
  return `${featureLabels[key] || key}: ${formatNumber(value)}`;
}

function readableProposal(id) {
  return proposalLabels[id] || id;
}

function renderCase(caseData) {
  caseImage.src = caseData.image;
  caseImage.alt = caseData.case_id;
  caseTitle.textContent = caseData.display_name;
  caseSummary.textContent = caseData.case_summary;
  questionEl.textContent = caseData.question;
  reviewGoalEl.textContent = caseData.review_goal;
  decisionEl.textContent = caseData.result.decision;
  decisionMeaningEl.textContent = decisionText[caseData.result.decision] || "";
  reasonEl.textContent = caseData.result.reason;

  regionOverlay.innerHTML = "";
  caseData.visual_graph.regions.forEach((region) => {
    const marker = document.createElement("div");
    marker.className = "region-marker";
    marker.style.left = `${region.x}%`;
    marker.style.top = `${region.y}%`;
    marker.style.width = `${region.w}%`;
    marker.style.height = `${region.h}%`;
    marker.innerHTML = `<strong>${region.label}</strong><span>${formatNumber(region.score)}</span>`;
    regionOverlay.appendChild(marker);
  });

  flowEl.innerHTML = "";
  caseData.visual_graph.stages.forEach((stage) => {
    const item = document.createElement("li");
    item.textContent = stage;
    flowEl.appendChild(item);
  });

  lensesEl.innerHTML = "";
  caseData.result.lenses.forEach((lens) => {
    const item = document.createElement("li");
    const featureText = Object.entries(lens.features)
      .map(([key, value]) => readableFeature(key, value))
      .join(", ");
    const maxValue = Math.max(...Object.values(lens.features).filter((value) => typeof value === "number"), 0);
    item.innerHTML = `
      <strong>${lensLabels[lens.lens_id] || lens.lens_id}</strong>
      <span>${featureText}</span>
      <i style="--bar:${Math.round(maxValue * 100)}%"></i>
    `;
    lensesEl.appendChild(item);
  });

  proposalsEl.innerHTML = "";
  caseData.result.proposals.forEach((proposal) => {
    const item = document.createElement("li");
    const selected = proposal.proposal_id === caseData.result.selected_proposal_id;
    item.className = selected ? "selected" : "";
    item.innerHTML = `
      <strong>${readableProposal(proposal.proposer_id)}</strong>
      <span>${selected ? "selected for review path" : "alternative route"}</span>
      <span>score ${formatNumber(proposal.score)} / confidence ${formatNumber(proposal.confidence)}</span>
      <i style="--bar:${Math.round(proposal.score * 100)}%"></i>
    `;
    proposalsEl.appendChild(item);
  });

  rejectedEl.innerHTML = "";
  if (caseData.result.rejected_proposals.length === 0) {
    const item = document.createElement("li");
    item.textContent = "None";
    rejectedEl.appendChild(item);
  } else {
    caseData.result.rejected_proposals.forEach((proposal) => {
      const item = document.createElement("li");
      item.innerHTML = `<strong>${readableProposal(proposal.proposer_id)}</strong><span>score ${formatNumber(proposal.score)} / confidence ${formatNumber(proposal.confidence)}</span>`;
      rejectedEl.appendChild(item);
    });
  }
  traceEl.textContent = JSON.stringify(caseData.result, null, 2);
}

cases.forEach((caseData, index) => {
  const option = document.createElement("option");
  option.value = String(index);
  option.textContent = caseData.display_name || caseData.case_id;
  caseSelect.appendChild(option);
});

caseSelect.addEventListener("change", () => renderCase(cases[Number(caseSelect.value)]));
renderCase(cases[0]);
