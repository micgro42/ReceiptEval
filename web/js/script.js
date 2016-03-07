'use strict';

jQuery(function(){
deform.load();

var chosen_config = {
    'search_contains': true,
    'width': '100%'
};

jQuery('.deformSeqAdd').click(function(event){jQuery('#purchaseForm select').chosen(chosen_config);});
jQuery('#purchaseForm select').chosen(chosen_config);
jQuery('#itemForm select').chosen({
    'search_contains': true,
    'width': 'auto'
});
jQuery('#itemForm').addClass('form-inline');
jQuery('#categoryForm').addClass('form-inline');
jQuery('fieldset').each(function(index){
$( this ).children().slice(1).wrapAll('<div class="panel-body">');
});
jQuery('fieldset').addClass('panel panel-default');
jQuery('legend').replaceWith(function(){
    return jQuery("<div />").append($(this).contents()).addClass('panel-heading');
});
})
