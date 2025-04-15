$("#saldo_utilizador").hide();
$("#esconder_saldo").hide();


$("#mostrar_saldo").click(function() {
    if ($("#saldo_utilizador").is(":visible")) {
        $("#mostrar_saldo").hide();
        $("#esconder_saldo").show();
        $("#saldo_utilizador").show();
    } else if ($("#esconder_saldo").is(":visible")) {
        $("#mostrar_saldo").show();
        $("#esconder_saldo").hide();
        $("#saldo_utilizador").hide();
    }
});