const buttonUIAction = (element) => {
    /** button UI actions when a button is clicked */

    // Toggle string values. 
    const toggleString = (something, string1, string2) => (something == string1 && string2 || string1)

    element.classList.toggle("btn-warning");
    element.classList.toggle("btn-primary");
    element.dataset.action = toggleString(element.dataset.action, 'add', 'remove')
    element.innerHTML = toggleString(element.innerHTML, 'Add to Watchlist', 'Remove from Watchlist')
}

const badgeUIAction = (badge, action) => {
    /** Badge UI handler for button click. */
    const count = parseInt(badge.innerText);
    badge.innerText = action === 'add'? count + 1 : count - 1;
}

window.addEventListener('DOMContentLoaded', () => {
    const watchlistButton = document.querySelector("#watchlist-button");
    const watchlistLinkBadge = document.querySelector("#watchlist-link > .badge");

    const watchlistButtonClickHandler = (event) => {
        const element = event.target;
        /** TODO API CALLS */
        badgeUIAction(watchlistLinkBadge, element.dataset.action)
        buttonUIAction(element);
    }

    if (watchlistButton) watchlistButton.addEventListener('click', watchlistButtonClickHandler);
})