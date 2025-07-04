const ul = document.getElementById("events");

async function fetchEvents() {
  const res = await fetch("/events");
  const data = await res.json();
  ul.innerHTML = "";
  data.forEach((e) => {
    let item = document.createElement("li");
    item.textContent = formatEvent(e);
    ul.appendChild(item);
  });
}

function formatEvent(e) {
  const date = new Date(e.timestamp).toUTCString();
  switch (e.event) {
    case "PUSH":
      return `${e.author} pushed to ${e.to_branch} on ${date}`;
    case "PULL_REQUEST":
      return `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${date}`;
    case "MERGE":
      return `${e.author} merged branch ${e.from_branch} to ${e.to_branch} on ${date}`;
    default:
      return "Unknown event";
  }
}

setInterval(fetchEvents, 15000);
fetchEvents();
