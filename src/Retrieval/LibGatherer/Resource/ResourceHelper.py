

class ResourceHelper:
    def ensurePathExists(self, path):
        """Makes sure a given path exists.
        Tries to create the given path, handles eventual failure.
        See: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python"""
        
        print "PathTool: Ensuring path %s exists." % path
        
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST: return
            if exc.errno == errno.ENOTDIR: return
            raise
        return

    def stripWhiteSpace(self, filename):
        """Substitutes all space literals (' ', '\n', '\t' etc.) with nothing."""
        filename = ' '.join(filename.spli())
        return filename
