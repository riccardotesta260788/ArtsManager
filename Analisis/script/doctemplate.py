from docxtpl import DocxTemplate

doc = DocxTemplate("template/doc/test.docx")
context = {'Titolo': "World company"}
doc.render(context)
doc.save("generated_doc.docx")
