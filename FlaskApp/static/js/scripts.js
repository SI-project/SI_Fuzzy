/**
 * Created by ariel on 31/10/19.
 */
function count_relevants_results() {
      var checks = $('input[type="checkbox"]').filter(':checked');
      var result = new Array();

      for(var i =0;i<checks.length;i++){
          result.push(checks[i].getAttribute('result_name'));
      }
      return result;
}