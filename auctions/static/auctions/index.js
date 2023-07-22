const MESSAGE_DIV = (message) => `<div class="messages ">
    <div class="alert alert-${message.tags}} alert-dismissible fade show" role="alert">
      ${message.text}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
</div>`;

const getCookie = (name) => {
  /**  Retrieve a cookie by name. */
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const apiCall = (element) => {
  /** Make an API call with the native fetch API. */
  const csrfToken = getCookie("csrftoken");
  const isAdd = element.dataset.action == "add" ? true : false;
  const method = isAdd ? "POST" : "DELETE";
  requestParams = {
    method,
    headers: { "X-CSRFToken": csrfToken },
    mode: "same-origin",
  };
  console.log(requestParams);
};

const buttonUIAction = (element) => {
  /** button UI actions when a button is clicked */

  // Toggle string values.
  const toggleString = (something, string1, string2) =>
    (something == string1 && string2) || string1;

  element.classList.toggle("btn-warning");
  element.classList.toggle("btn-primary");
  element.dataset.action = toggleString(
    element.dataset.action,
    "add",
    "remove"
  );
  element.innerHTML = toggleString(
    element.innerHTML,
    "Add to Watchlist",
    "Remove from Watchlist"
  );
};

const badgeUIAction = (badge, action) => {
  /** Badge UI handler for button click. */
  const count = parseInt(badge.innerText);
  badge.innerText = action === "add" ? count + 1 : count - 1;
};

const messageUIAction = (main, message, tags = "info") => {
  const oldMessages = document.querySelector(".messages");
  if (oldMessages) oldMessages.remove();

  const container = document.createElement("div");
  container.classList.add("messages", "p-2");
  const alert = document.createElement("div");
  alert.classList.add(
    "alert",
    `alert-${tags}`,
    "alert-dismissible",
    "fade",
    "show",
    "mb-0"
  );
  alert.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;
  container.appendChild(alert);
  main.prepend(container);
};

window.addEventListener("DOMContentLoaded", () => {
  const watchlistButton = document.querySelector("#watchlist-button");
  const watchlistLinkBadge = document.querySelector("#watchlist-link > .badge");
  const main = document.querySelector("main");

  const watchlistButtonClickHandler = (event) => {
    const element = event.target;
    const action = element.dataset.action;
    /** TODO API CALLS */
    apiCall(element);
    badgeUIAction(watchlistLinkBadge, action);
    buttonUIAction(element);
    action === "add"
      ? messageUIAction(main, "Item added to watchlist!")
      : messageUIAction(main, "Item removed watchlist!", "danger");
  };

  if (watchlistButton)
    watchlistButton.addEventListener("click", watchlistButtonClickHandler);
});
