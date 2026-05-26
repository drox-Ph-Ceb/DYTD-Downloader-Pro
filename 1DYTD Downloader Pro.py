    def on_tab_change(self):
        """Handle tab switching with proper synchronization to prevent race conditions."""
        # Prevent recursive calls during format mode sync
        if getattr(self, "_syncing_format", False):
            return

        try:
            mode = "mp3" if self.tabview.get() == "Audio Library" else "mp4"
        except Exception:
            mode = "mp3"

        # Prevent duplicate format switches
        try:
            current_mode = getattr(self, "_active_format_mode", None)
            if current_mode == mode:
                return  # Already in this mode, skip redundant sync
        except Exception:
            pass

        try:
            # ✅ KEY FIX: Pass preserve_playback=True to keep audio/video playing
            self._set_format_mode(mode, refresh_library=True, preserve_playback=True)
        except Exception as e:
            try:
                logger.exception("Tab format sync failed: %s", e)
                self._syncing_format = False  # Reset lock on error
            except Exception:
                pass
