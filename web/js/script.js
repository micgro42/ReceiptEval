'use strict';

jQuery(function(){
deform.load();

var chosen_config = {
    'search_contains': true
};

jQuery('.deformSeqAdd').click(function(event){jQuery('select').chosen(chosen_config);});
jQuery('select').chosen(chosen_config);
})
