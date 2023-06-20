// 全て選択選択で全チェックボックスをチェック
function AllChecked() {
    var all = document.form.all.checked;
    if (document.form.checks.length == undefined) {
        document.form.checks.checked = all;
        return
    }
    for (var i = 0; i < document.form.checks.length; i++) {
        document.form.checks[i].checked = all;
    }
}

// 個別のチェックボックスの選択解除で全て選択も解除
function DisChecked() {
    var checks = document.form.checks;
    var checksCount = 0;
    for (var i = 0; i < checks.length; i++) {
        if (checks[i].checked == false) {
            document.form.all.checked = false;
        } else {
            checksCount += 1;
            if (checksCount == checks.length) {
                document.form.all.checked = true;
            }
        }
    }
}