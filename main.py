from questions import QuestionMatcher
from DOCText import DocxToTextConverter
from screenshot import ScreenshotTaker
from coderunner import CProgramCompiler
from PDFGen import PDFGenerator, PDFMerger, ContentReader
from ui import PathSelector
import os
from OSchecker import OSChecker
from Folders import FolderCreator

folder_creator = FolderCreator()
folder_creator.create_folders()
os_checker = OSChecker()
os_name = os_checker.check_os()
path_selector = PathSelector()
docx_path, c_programs_path, screenshot_path = path_selector.get_paths()
ques_text = DocxToTextConverter(docx_path)
doc_text = ques_text.read_text_from_docx()
text_file_directory = "data"
text_file_path = text_file_directory+"/Questions.txt"
text_file = ques_text.create_text_file(text_file_path=text_file_path)
ques = QuestionMatcher(text_file_path, c_programs_path)
answered_questions = ques.matched_questions()
program_paths = ques.programs_paths()
executables_directory = "executables"

for i in range(0, len(program_paths)):
    print(f"\n------------------Question {i+1}------------------\n"
            f"{answered_questions[i]}\n"
            f"------------------Answer------------------\n")
    compiler = CProgramCompiler(program_path=f"{program_paths[i]}", 
                                executables_directory=executables_directory,
                                os=os_name)
    compiler.compile_and_run()
    current_program_name = ques.programs_names()[i]
    screenshot_taker = ScreenshotTaker(directory_path=screenshot_path,
                                        program_name=f"{current_program_name}")
    screenshot_taker.current_screenshots()
    screenshot_taker.take_screenshot()
    screenshot_taker.moving_screenshot()  

for i in range(0, len(program_paths)): 
    current_program_name = ques.programs_names()[i]
    pdf_generator = PDFGenerator(
        file_name=f"{current_program_name}",
        content_path=f"{program_paths[i]}",
        text = f"{answered_questions[i]}\n\n",
        content_reader=ContentReader,
        image_path=f"temp/{current_program_name}.jpg"
    )
    pdf_generator.create_pdf()
pdf_files_path = "pdf_files"
pdf_merger = PDFMerger(
    input_folder=pdf_files_path,
    output_file="Assignment.pdf"
)
pdf_merger.merge_pdfs()
