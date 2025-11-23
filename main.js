$(document).ready(function () {

    // Textillate configuration for main text animation.

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });
    
    //Siri configuration
    
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800, // Increased width for better display
        height: 180,
        style: "ios9",
        amplitude: 1,
        speed: 0.30,
        frequency: 4, // Added for better wave effect
        color: "#4895f0", // Custom color that matches your theme
        cover: true,
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeIn",
            sync: true,
        },
        out: {
            effect: "none",
            sync: true,
        },

    });

     // mic button click event (fixed: remove extra "()")
    $("#MicBtn").click(function () {
        startSiriUI();
        // call Python; eel.allCommands returns a Promise
        eel.allCommands()
            .then(function () { finishSiriUI(); })
            .catch(function (err) {
                console.error('allCommands error:', err);
                finishSiriUI();
                // ensure fallback UI state if Python didn't call ShowHood
                $("#Oval").attr("hidden", false);
                $("#SiriWave").attr("hidden", true);
            });
    });

    // helper to set siri text immediately (tries textillate-aware update, falls back)
    function setSiriMessage(text) {
        try {
            const formattedText = text.replace(/\s+/g, ' ')
                                     .replace(/\.\s/g, '.<br><br>')
                                     .replace(/\?\s/g, '?<br><br>')
                                     .replace(/\!\s/g, '!<br><br>');
            
            $(".siri-message").html(formattedText);
            
            // Restart textillate
            try { 
                $('.siri-message').textillate('start'); 
            } catch (e) { 
                console.log("Textillate error:", e);
            }
            
            // Scroll to show latest message
            $('.message-scroll-container').scrollTop($('.message-scroll-container')[0].scrollHeight);
            
        } catch (e) {
            console.warn("setSiriMessage error:", e);
            $(".siri-message").text(text);
        }
    }

    function startSiriUI() {
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        $("#MicBtn, #SendBtn").prop('disabled', true);
        $("#chatbox").prop('disabled', true);

        // show interim message while backend processes the request
        setSiriMessage("Wait, output generating...");
    }

    // helper to re-enable controls (UI switch back is done by Python via eel.ShowHood)
    function finishSiriUI() {
        $("#MicBtn, #SendBtn").prop('disabled', false);
        $("#chatbox").prop('disabled', false);
        updateInputButtons();
    }

    function doc_keyDown(e) {
        // prefer Ctrl+J or Alt+J on Windows
        if (e.key && e.key.toLowerCase() === 'j' && (e.ctrlKey || e.altKey || e.metaKey)) {
            e.preventDefault();
            startSiriUI();
            eel.allCommands()
                .then(function () { finishSiriUI(); })
                .catch(function (err) {
                    console.error('allCommands error:', err);
                    finishSiriUI();
                    $("#Oval").attr("hidden", false);
                    $("#SiriWave").attr("hidden", true);
                });
        }
    }
    document.addEventListener('keydown', doc_keyDown, false);

    // robust input / mic/send toggling
    const $micBtn = $("#MicBtn, #micBtn");
    const $sendBtn = $("#SendBtn, #sendBtn, .send-btn");
    const $chatbox = $("#chatbox, #ChatBox, input[name='chatbox']");

    if (!$chatbox.length) console.warn("chatbox element not found");
    if (!$micBtn.length) console.warn("mic button not found");
    if (!$sendBtn.length) console.warn("send button not found");

    $sendBtn.attr('hidden', true).hide();
    $micBtn.removeAttr('hidden').show();

    function updateInputButtons() {
      if (!$chatbox.length) return;
      const val = ($chatbox.val() || "").trim();
      if (val.length > 0) {
        $micBtn.attr('hidden', true).hide();
        $sendBtn.removeAttr('hidden').removeClass('d-none').css('display','inline-block').show();
      } else {
        $sendBtn.attr('hidden', true).hide();
        $micBtn.removeAttr('hidden').removeClass('d-none').css('display','inline-block').show();
      }
    }

    $chatbox.off('input paste keyup').on('input paste keyup', function () {
      // small delay for paste events
      setTimeout(updateInputButtons, 50);
    });
    updateInputButtons();

    // send action: show siri UI for typed queries then call Python with message
    function sendMessage() {
      const msg = ($chatbox.val() || "").trim();
      if (!msg) return;
      startSiriUI();
      try {
        eel.allCommands(msg)
            .then(function () { finishSiriUI(); })
            .catch(function (e) {
                console.error("Failed to call eel.allCommands:", e);
                finishSiriUI();
                $("#Oval").attr("hidden", false);
                $("#SiriWave").attr("hidden", true);
            });
      } catch (e) {
        console.error("call error:", e);
        finishSiriUI();
      }
      $chatbox.val('');
      updateInputButtons();
    }

    $sendBtn.off('click').on('click', sendMessage);
    $chatbox.off('keydown').on('keydown', function(e) {
      if (e.key === 'Enter') { e.preventDefault(); sendMessage(); }
    });
    
});
