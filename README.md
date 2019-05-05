### Introduction





### Procedures

1. **Fetching EIS documents**: All EIS documents, whether draft or final verisions, can be found on the dedicated Box.com repo (Permission must be granted by NEPA people). EIS douments that are stored on the Box repo do not have explicit file names (e.g. EIS-1234567), so in order to identify the required document, one should look up the file name in the accompanied Excel sheet. All EIS documents are archived, and they must be unarchived when downloaded. In most cases, an EIS archive contains several PDF files such as appendices, maps, reports, etc, so for the purposes of text re-use detection it is advisable to combine all PDFs into one txt file. This can be achieved using the accompanied bash script `eis_archive_to_txt.sh`
															`chmod +x eis_archive_to_txt.sh`

   ​							 `./eis_archive_to_txt.sh "Multispace-name Folder"`

   where `Multispace-name Folder` is the folder containing all PDFs of a single EIS document. This results in a merged `txt` file with the same name of the folder, e.g. `./"Multispace-name Folder".txt`

   **NOTE**: The bash script requires the installation of `pdftotext` utility, based on `xpdf` toolkit. Information on installation can be found on https://poppler.freedesktop.org and http://www.xpdfreader.com/support.html 
   
2. **Text Re-use**: the fraction of the text in the final version that was identified as being reused from the text in the draft version. In the context of EIS, we are interested in finding how much text has been reused from the draft version in the final version. This measure can be useful in detecting the working effiiency of a project if used with other variables such as `duration`, `File Size`, `Number of Unique Words`,etc. Text Re-use can be used via the following command:

3. ​								`python eis_text_reuse.py DRAFT_FOLDER FINAL_FOLDER`

        where `DRAFT_FOLDER` and `FINAL_FOLDER` are folders containing draft and final EIS repectively. 



​			The function `compare` in `eis_text_reuse.py` tests a suspicious document for near-duplicate plagiarism with regards to a source document and return the number of overlapping characters within an offset of 50 character long. To obtain the Text Re-use Score, we divide the number of shared characters between draft and final by the overall length of the final version

3. **Efficiency Detection**: The goal here is to predict the duration (in months) between the draft and the final version of EIS. To this end, we use the following variables:

   1. File_Size_Draft: the size in (megabytes) of the archive version of EIS draft
   
   2. File_Size_Final : the size in (megabytes) of the archive version of EIS final
   
   3. Unique_Words_Draft: Unique words in draft

   4. Unique_Words_Final: Unique words in draft
   
   5. Text_Reuse_Score: the number of shared characters between draft and final by the overall length of the final version
   
      
   
      To find the unique words for both 3 and 4, we use the following function:
   
      ```python
      def file_read(x):
        '''
        Takes a text file name and returns a set of unique words
        '''
        from nltk.tokenize import word_tokenize
        with open(x,'r',encoding='iso-8859-1') as file:
          txt = file.read() 
          tok = word_tokenize(txt)
          return set(tok)
      ```



Detecting the duration (in months) given the 5 variable above is a simple regression task. While there exist a number of regression algorithms, we choose decision tree due to its robustness as well as its interpretibabilty. The figure below shows how prediction decision is made by decision tree regression algorithm.

![](/Users/raghebal-ghezi/Github/Plagirism_Detection/eis-txt/tree.png)