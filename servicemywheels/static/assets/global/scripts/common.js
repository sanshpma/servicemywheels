$(function(){
	
	
	
	/*
	 * Form validation
	 */
	if($.fn.validate) {
		$('form.validate').each(function() {
			var validator = $(this).validate({
				ignore : 'input:hidden:not(:checkbox):not(:radio)',
				showErrors : function(errorMap, errorList) {
					this.defaultShowErrors();
					var self = this;
					$.each(errorList, function() {
						var $input = $(this.element);
						var $label = $input.parent().find('label.error').hide();
						if (!$label.length) {
							$label = $input.parent().parent().find('label.error');
						}
						if($input.is(':not(:checkbox):not(:radio):not(select):not([type=file])')) {
							$label.addClass('red');
							$label.css('width', '');
							$input.trigger('labeled');
						}
						$label.fadeIn();
					});
				},
                highlight: function (element) { // hightlight error inputs
                    $(element).closest('.form-group').addClass('has-error'); // set error class to the control group
                },
 
                unhighlight: function (element) { // revert the change done by hightlight
                    $(element).closest('.form-group').removeClass('has-error'); // set error class to the control group
                },
 
                success: function (label) {
                    label.closest('.form-group').removeClass('has-error'); // set success class to the control group
                },
				errorPlacement : function(error, element) {
					if(element.is(':not(:checkbox):not(:radio):not(select):not([type=file])')) {
						error.insertAfter(element);
					} else if(element.is('select')) {
						error.appendTo(element.parent());
					} else if (element.is('[type=file]')){
						error.insertAfter(element.parent());
					} else {
						error.appendTo(element.parent().parent());
					}
					
					if ($.browser.msie) {
						error.wrap('<div class="error-wrap" />');
					}
				}
			});
			

		});
		 //apply validation on select2 dropdown value change, this only needed for chosen dropdown integration.
            $('.validate select.select2box').change(function () {
                $('.validate').validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input
            });

            $('.validate .date-picker').change(function() {
                $('.validate').validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input 
            })
	}

	/*
	 * Reset form
	 */
	$('.reset-the-form').click(function() {
		 var form = $(".validate");
	    form.validate().resetForm();
	    form[0].reset();
	});

	
	/*
	 * Select2 - Select with search
	 */
	
	if($.fn.select2) {
		$('select.select2box').select2({
	        allowClear: true
	    });
		}
	
	/*
	 * Datepicker 
	 */

	if($.fn.datepicker) {	
	   	$('.date-picker').datepicker();
		}
	
	/*
	 * Chosen - Multi Select 
	 */
	if($.fn.chosen) {	
			$('.chosen-select').chosen({width: "inherit"});
			}
			
	/*
	 * Input File
	 */
		
	    $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
	        
	        var input = $(this).parents('.input-group').find(':text'),
	            log = numFiles > 1 ? numFiles + ' files selected' : label;
	        console.log(input);
	        if( input.length ) {
	            input.val(log);
	        } 
	        
	    });
		$(document).on('change', '.btn-file :file', function() {
			 
			  var input = $(this),
			  numFiles = input.get(0).files ? input.get(0).files.length : 1,
			  label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
			  input.trigger('fileselect', [numFiles, label]);
			 
			
		});
	/*
	 * Datatable
	 */	
	if($.fn.dataTable) {
		$('.datatable-this').dataTable();
	}
	
	
})

	/*
	 * Checkbox & Radio Re-init
	 */
	function radioCheckboxUpdate(id){
		 $.uniform.update(id);
	}

	/*
	 * Checkbox & Radio Init
	 */

	function radioCheckboxInit(id){
		 $(id).uniform();
	} 

	/*
	 * Select Box init
	 */

	function selectBoxInit(id){
		 $(id).select2();
	} 

	/*
	 * Select Box assign value
	 */

	function selectBoxAssign(id,value){
		 $(id).select2("val", value);
	} 

	/*
	 * Multi Select init
	 */

	 function multiSelectInit(id){
		 $(id).chosen({width: "inherit"});
	} 

	/*
	 * Multi Select assign value
	 */

	function multiSelectAssign(id,arr){
		 $(id).val(arr).trigger("chosen:updated");
	} 


	/*
	 * Loader - Inside portlet
	 */

	function showContainerLoader(id){
		Metronic.blockUI({
            target: $(id),
            animate: true,
            overlayColor: 'none'
        });
	} 

	function hideContainerLoader(id){
		Metronic.unblockUI($(id));
	} 
	
	function crm_loader_show(){
		Metronic.blockUI(); 
         $('.blockOverlay').attr('title','Click to unblock').click(Metronic.unblockUI); 
	}
	
	function crm_loader_hide(){
		Metronic.unblockUI();
	}
	
	function checkBoxUi(){
		$("input [type='checkbox']").uniform();
	}
	
	function selectOptionWidth(id){
		
	}