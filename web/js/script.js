'use strict';

jQuery(function(){
deform.load();

var chosen_config = {
    'search_contains': true,
    'width': '100%'
};

var updatePurchaseForm = function() {
    jQuery('#purchaseForm select').chosen(chosen_config);
    jQuery('#purchaseForm select[name=item_id]').change(function(event){
        var value = jQuery(this).val();
        var defaultCategory = jQuery(this).children().find('option[value='+value+']').parent('optgroup').attr('label');
        var $catSelect = jQuery(this).parents('.panel-body').first().find('select[name=category]')
        $catSelect.val(defaultCategory).trigger("chosen:updated");
    });
}
updatePurchaseForm();

jQuery('.deformSeqAdd').click(updatePurchaseForm);

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
