
var test = function(value,object) {
    console.log(object.children[0].innerHTML);
};


<script type="text/javascript">
    var dict= '{{ use_dict["00"] }}'
    console.log(dict)
    var test = function(obj) {
        console.log(obj.children[0].innerHTML);
    };

</script>