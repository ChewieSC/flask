(global-set-key [f2] 'undo)
(global-set-key [f3] 'find-file)
(global-set-key [f6] 'save-buffer)
(global-set-key [f5] 'save-buffer)
(global-set-key [f8] 'save-buffer)
(global-set-key [f7] 'save-buffer)
(global-set-key [f9] 'comment-region)
(global-set-key [f10] 'uncomment-region)
(global-set-key [(shift f7)] "\C-u\C-xs")
(global-set-key [f11] 'font-lock-fontify-buffer)
(global-set-key [(shift f11)] 'comment-region)
(global-set-key [f12] 'kill-this-buffer)
(global-set-key [kp-insert] 'nil)
(global-set-key [insert] 'nil)
(global-set-key "\C-a" 'beginning-of-line-text)
(global-set-key [(meta &)] 'query-replace-regexp)
(global-set-key "\C-xw" 'what-line)
(global-set-key [C-tab] 'other-window)
(global-set-key "\C-\M-l" 'switch-to-buffer-other-window)
(global-set-key "\C-z" 'yank)

;; (require 'tex); make shure AucTeX is available
;; (require 'xdvi-search "/data/MRW/allgemein/satz/lisp/allgemein/xdvi-search.el"); make shure xdvi-search is available

;;;\begin{stealing}{from=/usr/local/emacs-23.2/share/emacs/23.2/site-lisp/auctex/}
;re-definition for correct path to emacsclient exec until it is made customizable
;; (defun TeX-source-specials-view-expand-client () (concat "/usr/local/emacs-23.2/bin/emacsclient " TeX-source-specials-view-emacsclient-flags))
;;; \end{stealing} 


;; (add-hook 'LaTeX-mode-hook (lambda () 
;; 							 (server-start); make emacs find-able for external processes
;; 			     (setq TeX-source-specials-mode t); default-active src-special mode
;; 			     (setq TeX-source-correlate-mode t); default-active src-correlate mode
;; 			     (define-key LaTeX-mode-map (kbd "C-c C-f C-l") 'xdvi-jump-to-line));; make shortcut for xdvi-jump
;; )

;; (custom-set-variables
;;   ;; custom-set-variables was added by Custom.
;;   ;; If you edit it by hand, you could mess it up, so be careful.
;;   ;; Your init file should contain only one such instance.
;;   ;; If there is more than one, they won't work right.
;;  '(case-fold-search t)
;;  '(current-language-environment "Latin-9")
;;  '(default-input-method "latin-9-prefix")
;;  '(global-font-lock-mode t nil (font-lock))
;;  '(global-set-key (quote f2) t)
;;  '(inhibit-startup-screen t)
;;  '(scroll-bar-mode (quote right))
;;  '(show-paren-mode t nil (paren))
;;  '(tooltip-mode nil)
;;  '(uniquify-buffer-name-style (quote forward) nil (uniquify)))
(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(case-fold-search nil)
 '(column-number-mode t)
 '(current-language-environment "Latin-9")
 '(default-input-method "latin-9-prefix")
 '(delete-selection-mode 0)
 '(global-font-lock-mode t nil (font-lock))
 '(history-delete-duplicates t)
 '(history-length 500)
 '(inhibit-startup-screen t)
 '(ispell-library-path "/usr/lib/aspell")
 '(ispell-program-name "//usr/share/doc/aspell/examples/ispell")
 '(load-home-init-file t t)
 '(menu-bar-mode t)
 '(read-quoted-char-radix 10)
 '(rng-schema-locating-files (quote ("schemas.xml" "~/.emacs.d/schemas/schemas.xml" "/usr/local/emacs-23.2/share/emacs/23.2/etc/schema/schemas.xml")))
 '(safe-local-variable-values (quote ((TeX-master . "buch"))))
 '(save-place t nil (saveplace))
 '(savehist-additional-variables (quote (search-ring regexp-search-ring)))
 '(savehist-mode 1 nil (savehist))
 '(scroll-bar-mode nil)
 '(show-paren-mode t)
 '(show-paren-style (quote expression))
 '(tool-bar-mode nil)
 '(tramp-persistency-file-name nil)
 '(tramp-verbose 10)
 '(x-select-enable-clipboard t))

; (custom-set-faces
;   ;; custom-set-faces was added by Custom.
;   ;; If you edit it by hand, you could mess it up, so be careful.
;   ;; Your init file should contain only one such instance.
;   ;; If there is more than one, they won't work right.
;  '(default ((t (:inherit nil :stipple nil :background "black" :foreground "white" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 98 :width normal :foundry "unknown" :family "Helvetica")))))

;AUCTeX (only for le-tex sites)
;; (load "auctex.el" nil t t)
;; (load "preview-latex.el" nil t t)

;; (custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 ;; '(default ((t (:stipple nil :background "white" :foreground "black" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 150 :width normal :foundry "adobe" :family "courier"))))
 ;; '(blue ((t (:bold nil :foreground "blue" :background "grey70"))) t)
 ;; '(bold ((t (:bold nil :foreground "paleturquoise3" :background "black"))))
 ;; '(bold-italic ((t (:bold nil :italic nil))))
 ;; '(custom-button ((t (:size "14pt" :family "DejaVu Sans Mono" :bold t))))
 ;; '(custom-button-face ((t (:size "14pt" :family "DejaVu Sans Mono" :bold t))) t)
 ;; '(custom-documentation ((t (:bold nil))))
 ;; '(custom-documentation-face ((t (:bold nil))) t)
 ;; '(custom-face-tag ((t (:bold nil :underline t))))
 ;; '(custom-face-tag-face ((t (:bold nil :underline t))) t)
 ;; '(custom-group-tag ((((class color) (background light)) (:underline t :foreground "magenta"))))
 ;; '(custom-group-tag-face ((((class color) (background light)) (:underline t :foreground "magenta"))) t)
 ;; '(custom-state ((((class color) (background light)) (:bold nil :foreground "yellow"))))
 ;; '(custom-state-face ((((class color) (background light)) (:bold nil :foreground "yellow"))) t)
 ;; '(custom-variable-button ((t nil)))
 ;; '(custom-variable-button-face ((t nil)) t)
 ;; '(custom-variable-tag ((((class color) (background light)) (:bold nil :underline t :foreground "blue" :background "grey75"))))
 ;; '(custom-variable-tag-face ((((class color) (background light)) (:bold nil :underline t :foreground "blue" :background "grey75"))) t)
 ;; '(dired-face-directory ((t (:bold nil))))
 ;; '(dired-face-executable ((((class color)) (:foreground "red"))))
 ;; '(dired-perm-write ((t (:background "black" :foreground "white"))))
 ;; '(font-lock-comment-face ((t (:background "darkred" :foreground "yellow" :slant italic :weight normal :height .8 :family "DejaVu Sans Mono"))))
 ;; '(font-lock-doc-string-face ((t (:foreground "red" :background "black" :family "courier" :bold nil))))
 ;; '(font-lock-function-name-face ((t (:background "red" :foreground "black" :inverse-video t :weight normal))))
 ;; '(font-lock-keyword-face ((t (:bold nil :foreground "green" :background "black"))))
 ;; '(font-lock-preprocessor-face ((t (:bold nil :foreground "blue" :background "grey75"))))
 ;; '(font-lock-reference-face ((t (:bold nil :foreground "red"))))
 ;; '(font-lock-string-face ((t (:bold nil :foreground "yellow3"))))
 ;; '(font-lock-type-face ((t (:italic nil :foreground "green" :background "black"))))
 ;; '(font-lock-variable-name-face ((t (:bold nil :foreground "magenta"))))
 ;; '(highlight ((t (:foreground "black" :background "darkseagreen2"))))
 ;; '(hyper-apropos-documentation ((((class color) (background light)) (:foreground "darkred" :background "yellow"))))
 ;; '(hyper-apropos-hyperlink ((((class color) (background light)) (:foreground "blue4" :background "yellow"))))
 ;; '(isearch ((t (:foreground "black" :background "paleturquoise"))))
 ;; '(italic ((t (:bold nil :foreground "paleturquoise3"))))
 ;; '(left-margin ((t (:inverse-video t))) t)
 ;; '(message-highlighted-header-contents ((t (:bold nil :italic nil :underline t))))
 ;; '(mode-line-buffer-id ((t (:foreground "blue4" :background "Gray75"))))
 ;; '(modeline-mousable ((t (:foreground "firebrick" :background "Gray75"))) t)
 ;; '(nxml-cdata-section-content ((t (:inherit nxml-text :background "black" :foreground "orange"))))
 ;; '(nxml-cdata-section-delimiter ((t (:inherit nxml-delimiter :foreground "lightblue"))))
 ;; '(nxml-element-local-name ((t (:inherit default :background "black" :foreground "lightblue" :box nil))))
 ;; '(nxml-processing-instruction-delimiter ((t (:inherit nxml-delimiter :foreground "green"))))
 ;; '(nxml-tag-delimiter ((t (:inherit nxml-delimiter :foreground "lightblue"))))
 ;; '(paren-match ((t (:foreground "black" :background "darkseagreen2"))) t)
 ;; '(paren-mismatch ((t (:foreground "black" :background "DeepPink"))) t)
 ;; '(primary-selection ((t (:background "gray50"))) t)
 ;; '(right-margin ((t (:inverse-video t))) t)
 ;; '(secondary-selection ((t (:foreground "black" :background "paleturquoise"))))
 ;; '(set-face-attribute (quote default) nil :height)
 ;; '(underline ((t (:underline t :inverse-video t))))
 ;; '(widget-button ((t (:bold nil))))
 ;; '(widget-button-face ((t (:bold nil))) t)
 ;; '(widget-documentation ((((class color) (background light)) (:bold nil :foreground "blue"))))
 ;; '(widget-documentation-face ((((class color) (background light)) (:bold nil :foreground "blue"))) t)
 ;; '(widget-field ((((class grayscale color) (background light)) (:foreground "gray15" :background "gray85"))))
 ;; '(widget-field-face ((((class grayscale color) (background light)) (:foreground "gray15" :background "gray85"))) t)
;; )

(setq flyspell-large-region 1000000000)
(setq default-tab-width 3)

(defvar tex-verbatim-environments
  '("verbatim" "verbatim*" "lstlisting" "lstlisting*"))
(defvar tex-font-lock-syntactic-keywords
  '((eval . `(,(concat "^\\\\begin *{"
							 (regexp-opt tex-verbatim-environments t)
							 "}.*\\(\n\\)") 2 "|"))
(eval . `(,(concat "^\\(\\\\\\)end *{"
						 (regexp-opt tex-verbatim-environments t)
						 "}\\(.?\\)") (1 "|") (3 "<")))
("\\\\lstinline\\**\\([^a-z@*]\\)"
 1 (tex-font-lock-verb (match-end 1)))
("\\\\verb\\**\\([^a-z@*]\\)"
 1 (tex-font-lock-verb (match-end 1)))))

(require 'tex-mode)

(setq latex-mode-hook 
      '(lambda () 
	 (auto-fill-mode 1) 
	 (set-fill-column 100)
	 (abbrev-mode 1) 
	 (line-number-mode t) 
	 (define-key tex-mode-map "\C-c\C-m" 'latex-insert-macro)
	 (setq paragraph-start "^[ \t]*$\\|^[ \t]*\\\\begin.*$\\|^[ \t]*\\\\end.*$\\|^[ \t]*\\\\item.*$\\|^[ \t]*\\\\index.*$\\|^[ \t]*\\\\NeuerBegriff.*$\\|^[ \t]*\\\\bibitem.*$\\|.*[^\\\\]%.*$\\|[ \t]*}%?$")
	 (make-local-variable 'auto-fill-inhibit-regexp)
	 (setq auto-fill-inhibit-regexp "[^\\\\]%")
	 (make-local-variable 'paragraph-separate)
;	 (setq paragraph-separate "^[ \t]*$\\|^[ \t]*\\\\begin.*$\\|^[ \t]*\\\\end.*$\\|^[ \t]*\\\\item.*$\\|^[ \t]*\\\\index.*$\\|^[ \t]*\\\\NeuerBegriff.*$\\|.*[^\\\\]%.*$\\|[ \t]*}%?$")
	 (setq paragraph-separate "[ \t\n]$\\|.*[^\\\\]%.*$\\|^[ \t]*\\\\begin.*$\\|^[ \t]*\\\\end.*$")
	 (defvar tex-font-lock-keywords 
	   (("\\\\\\(begin\\|end\\|newcommand\\){\\([a-zA-Z0-9\\*]+\\)}"
	     2 font-lock-function-name-face)
	    ("\\(\\(^%\\|[^\\\\]%\\)\\)$" 1 font-lock-comment-face)
	    ("\\\\\\(cite\\|gllabel\\|label\\|pageref\\|ref\\){\\([^}
	   \t\n]+\\)}" 2 font-lock-reference-face) ("^[
	   \t]*\\\\def\\\\\\(\\(\\w\\|@\\)+\\)" 1
	   font-lock-function-name-face) "\\\\\\([a-zA-Z@]+\\|.\\)"
	    ("\\\\emph{\\([^}]+\\)}" 1 'italic keep)
	    ("\\\\text\\(\\(bf\\)\\|it\\|sl\\){\\([^}]+\\)}" 3 (if
								   (match-beginning 2) 'bold 'italic) keep)
	    ("\\\\\\(\\(bf\\)\\|em\\|it\\|sl\\)\\>\\(\\([^}&\\]\\|\\\\[^\\]\\)+\\)"
	     3 (if (match-beginning 2) 'bold 'italic) keep)))
	 ))

(setq text-mode-hook 
      '(lambda () (auto-fill-mode 1) ))

;; This adds additional extensions which indicate files normally
;; handled by cc-mode.
(setq auto-mode-alist
      (append '(("Makefile" . makefile-mode)
		("\\.mk$" . makefile-mode)
		("\\.C$"  . c++-mode)
		("\\.cc$" . c++-mode)
		("\\.hh$" . c++-mode)
		("\\.h$"  . c++-mode)
		("\\.c$"  . c-mode)
		("\\.texfig$". latex-mode)
		("\\.sty$". latex-mode)
		("\\.cls$". latex-mode)
		("\\.cap$". latex-mode)
		("\\.tex$"  . latex-mode)
		("\\.tab$"  . latex-mode)
		("\\.xmt$"  . latex-mode)
		("\\.ltx$"  . latex-mode))
	      auto-mode-alist))


;; (define-key global-map [(backspace)] 'backward-delete-char-untabify)
 ;; (load "/home/mops/makros/journal-functions.el")
 ;; (load "/home/mops/makros/giovanni.el")
 ;; (load "/home/moriz/makros/tables.el")
 ;; (load "/home/mops/makros/mops.el")
 (load "~/felix.el")
 ;; (load "/home/nailimix/max.el")
 ;; (load "/local-data/journal/Journal-base/elisp/xml-tools/xml-wiley-indent.el")
 ;; (load "/local-data/journal/Journal-base/gnulisp/BASE/base.el")

(set-variable 'ps-paper-type 'a4)
(setq minibuffer-max-depth nil)
(setq visible-bell t) 

(setq w32-pass-lwindow-to-system nil)
(setq w32-lwindow-modifier 'super)

(defun nxml-pretty-print-xml-region (begin end)
  (interactive "r")
  (save-excursion
      (nxml-mode)
      (goto-char begin)
      (while (search-forward-regexp "\>[ \\t]*\<" nil t)
        (backward-char) (insert "\n"))
      (indent-region begin end))
    (message "Ah, much better!")
)

(defun m-nxml-mode-hook ()
"key definitions for nxml mode"
(interactive)
(set-variable 'fill-column 100)
; nxml key bindings consistent with C-b, C-f, C-p, C-n, M-b, M-f, M-p, M-n
(define-key nxml-mode-map "\C-of" 'nxml-forward-balanced-item)     ; f for forward
(define-key nxml-mode-map "\C-ob" 'nxml-backward-balanced-item)    ; b for backward
(define-key nxml-mode-map "\C-op" 'nxml-backward-element)   ; p consistent with C-p
(define-key nxml-mode-map "\C-on" 'nxml-forward-element)  ;
(define-key nxml-mode-map "\M-of" 'nxml-forward-element)     ; f for forward, 
(define-key nxml-mode-map "\M-ob" 'nxml-backward-element)    ; b for backward
(define-key nxml-mode-map "\M-op" 'nxml-backward-paragraph)   ; p consistent with M-p
(define-key nxml-mode-map "\M-on" 'nxml-forward-paragraph)  ;
;(define-key nxml-mode-map "\M-ou" 'nxml-backward-up-element) ; u for up
;(define-key nxml-mode-map "\M-od" 'nxml-down-element)        ; d for down
(define-key nxml-mode-map "\M-ok" 'nxml-kill-element)        ; d for down

(define-key nxml-mode-map [M-insert] 'nxml-copy-tag-contents)
(define-key nxml-mode-map "\C-xw" 'nxml-kill-tag-contents)

(define-key nxml-mode-map "\C-cv" 'browse-url-of-buffer) ; should be consistent with the shortcut in the html-mode
(set-variable 'tab-width 2)

  (message "Defined extra key-bindings for nxml-mode")
)
(add-hook 'nxml-mode-hook 'm-nxml-mode-hook)

(prefer-coding-system 'utf-8) (set-default-coding-systems 'utf-8); avoid taking UTF-8 files as ISO-8859-x


;;; GOOGLE CALENDAR ERWEITERUNG
;; (setq load-path (append (list (expand-file-name "~/icalendar")) load-path))
;; (require 'icalendar)

;; (setq load-path (append load-path (list (expand-file-name "~/google"))))
;; (require 'google-calendar)

;; (setq google-calendar-user           "konrad.ehrenfeld@googlemail.com")         ;;; GOOGLE USER
;; (setq google-calendar-code-directory "~/google/code") ;;; PATH TO THE PYTHON CODE
;; (setq google-calendar-directory      "~/tmp")               ;;; TEMPORARY DIRECTORY
;; (setq google-calendar-url            "https://www.google.com/calendar/ical/4v51415dv31kg9pjvuca8f3m7s%40group.calendar.google.com/private-3729401c43b5c2903374801eaa877852/basic.ics")  ;;; URL TO YOUR GOOGLE CALENDAR
;; (setq google-calendar-auto-update    t)                    ;;; DEFINE IF THE CALENDAR IS DOWNLOADED AFTER EVERY MODIFICATION

;; (google-calendar-download);
(put 'upcase-region 'disabled nil)

