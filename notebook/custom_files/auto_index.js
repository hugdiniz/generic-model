    function generateIndex()
    {
        html = "<ol>";
        
        lists = $(".list");
        for(i=0;i<lists.length;i++)
        {
            html = html + "<li><a href='#"+lists[i].id+"'>"+lists[i].innerText+"</a></li>"
        }
        $("#index").html(html+"</ol>");
    }
    
    $(function() {
        generateIndex();
    });