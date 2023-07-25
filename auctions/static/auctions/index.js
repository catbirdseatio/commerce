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

const apiCall = async (element, pk, main) => {
  /** Make an API call with the native fetch API. 
   * 
   * element: the button ui element
   * pk: primary key of listing.
   * main: the <main> tag. The message returned from API is prepended to main.
  */
  const baseURL = `watchlist/${pk}`
  const csrfToken = getCookie("csrftoken");
  const isAdd = element.dataset.action == "add" ? true : false;
  const method = isAdd ? "POST" : "DELETE";
  const requestParams = {
    method,
    headers: { "X-CSRFToken": csrfToken },
    mode: "same-origin",
  };
  return fetch(baseURL, requestParams)
    .then((response) => response.json()) 
      .then((data) => {
          messageUIAction(main, data.message, data.tags)
      }).catch((err) => {
          console.log(err);
      }) 
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
/** Add an alert message to the UI **/

  // Remove old messages if there are any
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

  /** Event handlers */
  const watchlistButtonClickHandler = (event) => {
    const element = event.target;
    const action = element.dataset.action;
    const pk = element.dataset.pk;
    let message;

    apiCall(element, pk, main)
    badgeUIAction(watchlistLinkBadge, action);
    buttonUIAction(element);
    action === "add"
      ? messageUIAction(main, message)
      : messageUIAction(main, message, "danger");
  };

  /** Event listeners */
  if (watchlistButton)
    watchlistButton.addEventListener("click", watchlistButtonClickHandler);
});
