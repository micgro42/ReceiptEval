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
    jQuery('#purchaseForm select[name=item_id]').change();

    jQuery('input[name=price]').change(function(e){
        var sum = 0;
        jQuery('input[name=price]').each((index, elem) => {sum += Number(jQuery(elem).val())});
        console.log("price updated. new total: " + sum);
        jQuery('#total').text(Math.round(sum*100)/100);
    });
}
updatePurchaseForm();

jQuery('.deform-seq-add').click(updatePurchaseForm);

jQuery('#itemForm select').chosen(chosen_config);
// jQuery('#itemForm').addClass('form-inline');
// jQuery('#categoryForm').addClass('form-inline');
jQuery('fieldset').each(function(index){
$( this ).children().slice(1).wrapAll('<div class="panel-body">');
});
jQuery('fieldset').addClass('panel panel-default');
jQuery('legend').replaceWith(function(){
    return jQuery("<div />").append($(this).contents()).addClass('panel-heading');
});
jQuery('#purchaseForm').append(jQuery('<div id="total" class="bg-info">0</div>'));

jQuery('#itemForm').submit(function(evt){
    evt.preventDefault();
    evt.stopPropagation();
    var $this = jQuery(this);
    jQuery.ajax({
        type: 'PUT',
        data: {
            form: "itemForm",
            name: $this.find('input[name=name]').val(),
            category: $this.find('select[name=category]').val(),
            comment: $this.find('input[name=comment]').val(),
        }
    }).done(function(){
        $this.css('background-color','green');
    }).fail(function(){
        $this.css('background-color','red');
    });
});


})
