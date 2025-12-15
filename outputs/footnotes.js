document.addEventListener('DOMContentLoaded', function () {
	var tooltip = null;

	function createTooltip() {
		if (!tooltip) {
			tooltip = document.createElement('div');
			tooltip.className = 'footnote-tooltip';
			document.body.appendChild(tooltip);
		}
		return tooltip;
	}

	function showTooltip(sup, content) {
		var tip = createTooltip();
		tip.innerHTML = content;
		tip.style.display = 'block';

		var rect = sup.getBoundingClientRect();
		var tipRect = tip.getBoundingClientRect();

		// Position below the reference
		tip.style.left = Math.max(10, rect.left + window.scrollX - tipRect.width / 2 + rect.width / 2) + 'px';
		tip.style.top = (rect.bottom + window.scrollY + 5) + 'px';

		// Keep tooltip on screen
		if (rect.left + window.scrollX - tipRect.width / 2 < 10) {
			tip.style.left = '10px';
		}
		if (rect.left + window.scrollX + tipRect.width / 2 > window.innerWidth - 10) {
			tip.style.left = (window.innerWidth - tipRect.width - 10) + 'px';
		}
	}

	function hideTooltip() {
		if (tooltip) {
			tooltip.style.display = 'none';
		}
	}

	// Find all footnote references
	var footnoteRefs = document.querySelectorAll('sup[id^="fnref"]');
	footnoteRefs.forEach(function(sup) {
		var link = sup.querySelector('a[href^="#fn"]');
		if (!link) return;

		var fnId = link.getAttribute('href').substring(1);
		var footnote = document.getElementById(fnId);
		if (!footnote) return;

		// Get footnote content without the back link
		var content = footnote.cloneNode(true);
		var backlink = content.querySelector('a[href^="#fnref"]');
		if (backlink) {
			backlink.remove();
		}

		sup.addEventListener('mouseenter', function() {
			showTooltip(sup, content.innerHTML);
		});

		sup.addEventListener('mouseleave', function() {
			hideTooltip();
		});

		// Keep footnote link working
		link.addEventListener('click', function() {
			hideTooltip();
		});
	});
});
