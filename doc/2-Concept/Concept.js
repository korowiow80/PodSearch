$(function() {
    // Deck initialization
    $.deck('.slide');

    $.extend(true, $.deck.defaults, {
        selectors: {
            statusCurrent: '.deck-status-current',
            statusTotal: '.deck-status-total'
        },

        countNested: false
    });
});
