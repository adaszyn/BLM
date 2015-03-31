/**
 * Created by wojciech on 31.03.15.
 */
    $(document).ready(function () {

               $("#frontphrase1").fadeIn("normal");
        setTimeout(function () {
            $("#frontphrase2").fadeIn("normal");
            setTimeout(function () {
                               $(".arrowframe").show("slow");

        }, 1000);
        }, 1000);

    });