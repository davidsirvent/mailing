Quill.register("modules/htmlEditButton", htmlEditButton);

var quill = new Quill('#editor', {
    /* Original complete toolbar */
    /* https://github.com/KillerCodeMonkey/ngx-quill/issues/295 */

    modules: {
        htmlEditButton: {}, /* https://github.com/benwinding/quill-html-edit-button */
        'syntax': false,
        'toolbar': [
            [{ 'font': [] }, { 'size': [] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'script': 'super' }, { 'script': 'sub' }],
            [{ 'header': '1' }, { 'header': '2' }, 'blockquote', 'code-block'],
            [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'indent': '-1' }, { 'indent': '+1' }],
            ['direction', { 'align': [] }],
            ['link', 'image', 'video'],
            ['clean']
        ]
    },
    theme: 'snow'
});