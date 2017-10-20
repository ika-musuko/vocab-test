<html>
<head>
    <title>vocab test</title>
    <link rel="stylesheet" type="text/css" href="default.css"/>
    <script>
    </script>
</head>

<body>
    <div class="questionbox">
        <h3 style="white-space:nowrap;">{{number}} of {{total}}. Choose the description that best matches the word <div class="word" style="color:blue;">{{query}}</div></h3>
        <form action="/respond" method="POST" id="answer_form">
            <div style="display:block;">
            %for l, c in zip(letters, choices):
            <input class="choice" type="radio" name="answer" value="{{l}}">{{l}}. {{c.definition}} <br/>
            %end
            <input class="submit" type="submit" value="next" name="next_button">
            </div>
        </form>
    </div>
</body>
</html>
