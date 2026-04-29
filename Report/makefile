TEX = pdflatex
DOC = Report
IMAGES = othello.png main_menu.png leaderboard.png stats.png

# Rule to build PDF, depending on tex and image files
$(DOC).pdf: $(DOC).tex $(IMAGES)
	$(TEX) $(DOC).tex
	$(TEX) $(DOC).tex # Run twice for proper referencing

clean:
	rm -f *.aux *.log *.pdf
