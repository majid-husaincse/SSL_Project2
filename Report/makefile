<<<<<<< HEAD
TEX = pdflatex
DOC = Report
IMAGES = othello.png main_menu.png leaderboard.png stats.png

.PHONY: all clean

all: $(DOC).pdf


# Rule to build PDF, depending on tex and image files
$(DOC).pdf: $(DOC).tex $(IMAGES)
	$(TEX) $(DOC).tex
	$(TEX) $(DOC).tex # Run twice for proper referencing

clean:
	rm -f *.aux *.log *.pdf *.out
=======
Report.pdf: Report.tex
	pdflatex Report
.PHONY: clean
clean: 
	rm *.aux *.toc *.out *.log
>>>>>>> main
