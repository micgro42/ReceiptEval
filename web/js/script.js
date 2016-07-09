
jQuery(function(){
'use strict';
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

var $itemForm = jQuery('#itemForm');
$itemForm.css('position', 'fixed');
$itemForm.hide();
var $itemFormButton = jQuery('<button id="showItemForm" class="showForm">New Item</button>');
$itemFormButton.click(function(evt){
    $itemForm.slideDown();
});
jQuery('body').append($itemFormButton);
$itemForm.submit(function(evt){
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
        $this.slideUp();
    }).fail(function(){
        $this.css('background-color','red');
    });
});

var $categoryForm = jQuery('#categoryForm');
$categoryForm.css('position', 'fixed');
$categoryForm.hide();
var $categoryFormButton = jQuery('<button id="showCategoryForm" class="showForm">New Category</button>');
$categoryFormButton.click(function(evt){
    $categoryForm.slideDown();
});
jQuery('body').append($categoryFormButton);
$categoryForm.submit(function(evt){
    evt.preventDefault();
    evt.stopPropagation();
    var $this = jQuery(this);
    jQuery.ajax({
        type: 'PUT',
        url: window.location.pathname + 'category/',
        data: {
            form: "categoryForm",
            name: $this.find('input[name=name]').val(),
            comment: $this.find('input[name=comment]').val(),
        }
    }).done(function(data, textStatus, jqXHR){
        window.catData = data;
        var $catsel = jQuery('select[name=category]');
        $catsel.empty();
        jQuery.each(jQuery.parseJSON(data), function (key, value) {
            $catsel.append(jQuery('<option><option>').val(value[0]).text(value[1]));
        });
        $catsel.trigger('chosen:updated');
        $this.slideUp();
    }).fail(function(){
        $this.css('background-color','red');
    });
});

})
