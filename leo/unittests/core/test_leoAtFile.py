#@+leo-ver=cub-1-thin
#@0 [ekr.20210901172411.1] @f ../unittests/core/test_leoAtFile.py
"""Tests of leoAtFile.py"""

import os
import tempfile
from leo.core import leoGlobals as g
from leo.core import leoAtFile
from leo.core import leoBridge
from leo.core.leoTest2 import LeoUnitTest


#@+others
#@> class TestAtFile(LeoUnitTest)
class TestAtFile(LeoUnitTest):
    """Test cases for leoAtFile.py"""

    def setUp(self):
        # Create a pristine instance of the AtFile class.
        super().setUp()
        self.at = leoAtFile.AtFile(self.c)

    #@+others
    #@>  TestAtFile.bridge
    def bridge(self):
        """Return an instance of Leo's bridge."""
        return leoBridge.controller(
            gui='nullGui',
            loadPlugins=False,
            readSettings=False,
            silent=True,
            verbose=False,
        )

    #@ TestAtFile.test_bug_1469
    def test_bug_1469(self):
        # Test #1469: saves renaming an external file
        # https://github.com/leo-editor/leo-editor/issues/1469
        # Create a new outline with @file node and save it
        bridge = self.bridge()
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = f"{temp_dir}{os.sep}test_file.leo"
            c = bridge.openLeoFile(filename)
            p = c.rootPosition()
            p.h = '@file 1'
            p.b = 'b1'
            c.save()
            # Rename the @file node and save
            p1 = c.rootPosition()
            p1.h = "@file 1_renamed"
            c.save()
            # Remove the original "@file 1" from the disk
            external_filename = f"{temp_dir}{os.sep}1"
            assert os.path.exists(external_filename), external_filename
            os.remove(external_filename)
            assert not os.path.exists(external_filename), external_filename
            # Change the @file contents, save and reopen the outline
            p1.b = "b_1_changed"
            c.save()
            c.close()
            c = bridge.openLeoFile(c.fileName())
            p1 = c.rootPosition()
            self.assertEqual(p1.h, "@file 1_renamed")

    #@ TestAtFile.test_bug_1889_tilde_in_at_path
    def test_bug_1889_tilde_in_at_path(self):
        # Test #1889: Honor ~ in ancestor @path nodes.
        # Create a new outline with @file node and save it
        bridge = self.bridge()
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = f"{temp_dir}{os.sep}test_file.leo"
            c = bridge.openLeoFile(filename)
            root = c.rootPosition()
            root.h = '@path ~/sub-directory/'
            child = root.insertAsLastChild()
            child.h = '@file test_bug_1889.py'
            child.b = '@language python\n# test #1889'
            path = c.fullPath(child)
            assert '~' not in path, repr(path)

    #@ TestAtFile.test_bug_3272_at_path
    def test_bug_3272_at_path(self):
        #  @path bookmarks
        #    @file at_file_test.py
        c = self.c
        root = c.rootPosition()
        root.h = '@path bookmarks'
        child = root.insertAsLastChild()
        child.h = '@file at_file_test.py'
        path = c.fullPath(child)
        expected = 'bookmarks/at_file_test.py'
        self.assertTrue(path.endswith(expected))

    #@ TestAtFile.test_checkPythonSyntax
    def test_checkPythonSyntax(self):
        at, p = self.at, self.c.p

        # dedent is required.
        s = self.prep('''
            # no error
            def spam():
                pass
        ''')
        assert at.checkPythonSyntax(p, s), 'fail 1'

        s2 = self.prep('''
            # syntax error
            def spam:  # missing parens.
                pass
        ''')

        assert not at.checkPythonSyntax(p, s2), 'fail2'

    #@ TestAtFile.test_directiveKind4
    def test_directiveKind4(self):
        at = self.at
        at.language = 'python'  # Usually set by atFile read/write logic.
        table = [
            ('@=', 0, at.noDirective),
            ('@', 0, at.atDirective),
            ('@ ', 0, at.atDirective),
            ('@\t', 0, at.atDirective),
            ('@\n', 0, at.atDirective),
            ('@all', 0, at.allDirective),
            ('    @all', 4, at.allDirective),
            ('    @all', 0, at.allDirective),  # 2021/11/04
            ("@c", 0, at.cDirective),
            ("@code", 0, at.codeDirective),
            ("@doc", 0, at.docDirective),
            ('@others', 0, at.othersDirective),
            ('    @others', 4, at.othersDirective),
            # ("@end_raw", 0, at.endRawDirective), # #2276.
            # ("@raw", 0, at.rawDirective), # #2276.
        ]
        for name in g.globalDirectiveList:
            # Note: entries in g.globalDirectiveList do not start with '@'
            if name not in (
                'all',
                'c',
                'code',
                'doc',
                'end_raw',
                'others',
                'raw',
            ):
                table.append(
                    ('@' + name, 0, at.miscDirective),
                )
        for s, i, expected in table:
            result = at.directiveKind4(s, i)
            self.assertEqual(result, expected, msg=f"i: {i}, s: {s!r}")

    #@ TestAtFile.test_directiveKind4_2
    def test_directiveKind4_2(self):
        at = self.at
        at.language = 'python'  # Usually set by atFile read/write logic.
        table = (
            (at.othersDirective, '@others'),
            (at.othersDirective, '@others\n'),
            (at.othersDirective, '    @others'),
            (at.miscDirective,   '@tabwidth -4'),
            (at.miscDirective,   '@tabwidth -4\n'),
            (at.miscDirective,   '@encoding'),
            (at.noDirective,     '@encoding.setter'),
            (at.noDirective,     '@encoding("abc")'),
            (at.noDirective,     'encoding = "abc"'),
            (at.noDirective,     '@directive'),  # A crucial new test.
            (at.noDirective,     '@raw'),  # 2021/11/04.
        )  # fmt: skip
        for expected, s in table:
            result = at.directiveKind4(s, 0)
            self.assertEqual(expected, result, msg=repr(s))

    #@ TestAtFile.test_findSectionName
    def test_findSectionName(self):
        # Test code per #2303.
        at, p = self.at, self.c.p
        at.initWriteIvars(p)
        ref = g.angleBrackets(' abc ')
        table = (
            (True,  f"{ref}\n"),
            (True,  f"{ref}"),
            (True,  f"  {ref}  \n"),
            (False, f"if {ref}:\n"),
            (False, f"{ref} # comment\n"),
            (False, f"# {ref}\n"),
        )  # fmt: skip
        for valid, s in table:
            name, n1, n2 = at.findSectionName(s, 0, p)
            self.assertEqual(valid, bool(name), msg=repr(s))

    #@ TestAtFile.test_parseLeoSentinel
    def test_parseLeoSentinel(self):
        at = self.at
        table = (
            # start, end, new_df, isThin, encoding
            # pre 4.2 formats...
            ('#', '',    False, True,  'utf-8',  '#@+leo-thin-encoding=utf-8.'),
            ('#', '',    False, False, 'utf-8',  '#@+leo-encoding=utf-8.'),
            # 4.2 formats...
            ('#', '',    True,  True,  'utf-8',  '#@+leo-ver=4-thin-encoding=utf-8,.'),
            ('/*', '*/', True,  True,  'utf-8',  r'\*@+leo-ver=5-thin-encoding=utf-8,.*/'),
            ('#', '',    True,  True,  'utf-8',  '#@+leo-ver=5-thin'),
            ('#', '',    True,  True,  'utf-16', '#@+leo-ver=5-thin-encoding=utf-16,.'),
        )  # fmt: skip
        try:
            for start, end, new_df, isThin, encoding, s in table:
                valid, new_df2, start2, end2, isThin2 = at.parseLeoSentinel(s)
                # g.trace('start',start,'end',repr(end),'len(s)',len(s))
                assert valid, s
                self.assertEqual(new_df, new_df2, msg=repr(s))
                self.assertEqual(isThin, isThin2, msg=repr(s))
                self.assertEqual(end, end2, msg=repr(s))
                self.assertEqual(at.encoding, encoding, msg=repr(s))
        finally:
            at.encoding = 'utf-8'

    #@ TestAtFile.test_putBody_adjacent_at_doc_part
    def test_putBody_adjacent_at_doc_part(self):
        at, c = self.at, self.c
        root = c.rootPosition()
        root.h = '@file test.html'
        contents = self.prep(
            '''
    #@@doc
            First @doc part
    #@@doc
            Second @doc part
        '''
        )
        expected = self.prep(
            '''
            <!--@+doc-->
            <!--
            First @doc part
            -->
            <!--@+doc-->
            <!--
            Second @doc part
            -->
        '''
        )
        root.b = contents
        at.initWriteIvars(root)
        at.putBody(root)
        result = ''.join(at.outputList)
        if result != expected:
            g.trace('language:', c.atFileCommands.language)
            g.printObj(expected, tag='expected')
            g.printObj(result, tag='result')
        self.assertEqual(result, expected)

    #@ TestAtFile.test_putBody_at_doc_part_indent_in_leaf
    def test_putBody_at_doc_part_indent_in_leaf(self):
        # #4864: a doc part nested inside a leaf node's own (unsplit) block
        # must get sentinels indented to match the surrounding code, and the
        # result must round-trip losslessly and stay stable on re-derivation.
        at, c = self.at, self.c
        root = c.rootPosition()
        root.h = '@file test_4864.py'
        # The '@' and '@c' directives *must* be at column 0: only nearby
        # code lines carry the leaf's own literal indentation.
        root.b = "def foo():\n    a = 1\n@ A nested doc part\n    Line 2.\n@c\n    b = 2\n"
        at.initWriteIvars(root)
        at.putBody(root)
        result = ''.join(at.outputList)
        expected = (
            "def foo():\n"
            "    a = 1\n"
            "    # @+at A nested doc part\n"
            "    #     Line 2.\n"
            "    # @@c\n"
            "    b = 2\n"
        )
        self.assertEqual(result, expected)

        # Full round trip: derive, read back purely in memory, re-derive.
        # The second derivation must be byte-identical to the first: #4864
        # was a bug where sentinel indentation drifted on every save.
        at.initWriteIvars(root)
        at.sentinels = True
        at.outputList = []
        at.putFile(root, sentinels=True)
        derived1 = ''.join(at.outputList)
        ok = leoAtFile.FastAtRead(c, c.fileCommands.gnxDict).read_into_root(
            derived1, 'test_4864.py', root
        )
        self.assertTrue(ok)
        at2 = leoAtFile.AtFile(c)
        at2.initWriteIvars(root)
        at2.sentinels = True
        at2.outputList = []
        at2.putFile(root, sentinels=True)
        derived2 = ''.join(at2.outputList)
        self.assertEqual(derived1, derived2)

    #@ TestAtFile.test_putBody_at_all
    def test_putBody_at_all(self):
        at, c = self.at, self.c
        root = c.rootPosition()
        root.h = '@file test.py'
        child = root.insertAsLastChild()
        child.h = 'child'
        child.b = self.prep(
            '''
            def spam():
                pass

            @ A single-line doc part.
        '''
        )

        child.v.fileIndex = '<GNX>'
        contents = '''ATall'''.replace('AT', '@')
        expected_contents = self.prep('''
            #AT+all
            #AT+node:<GNX>: ** child
            def spam():
                pass

            @ A single-line doc part.
            #AT-all
        ''').replace('AT', '@')
        test_s = contents.replace('#@', '# @')
        expected = expected_contents.replace('#@', '# @')

        root.b = test_s
        at.initWriteIvars(root)
        at.putBody(root)
        results = ''.join(at.outputList)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestAtFile.test_putBody_at_all_after_at_doc
    def test_putBody_at_all_after_at_doc(self):
        at, c = self.at, self.c
        root = c.rootPosition()
        root.h = '@file test.py'
        contents = self.prep(
            '''
            ATdoc
            doc line 1
            ATall
        '''
        ).replace('AT', '@')

        # Only @c or @code end an @doc part.
        # Therefore, the @all line is part of the @doc part.
        expected_contents = self.prep(
            '''
            #AT+doc
            # doc line 1
            # ATall
        '''
        ).replace('AT', '@')
        test_s = contents.replace('#@', '# @')
        expected = expected_contents.replace('#@', '# @')

        root.b = test_s
        at.initWriteIvars(root)
        at.putBody(root)
        results = ''.join(at.outputList)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestAtFile.test_putBody_at_others
    def test_putBody_at_others(self):
        at, c = self.at, self.c
        root = c.rootPosition()
        root.h = '@file test_putBody_at_others.py'
        child = root.insertAsLastChild()
        child.h = 'child'
        child.b = '@others\n'
        child.v.fileIndex = '<GNX>'
        contents = '''ATothers'''.replace('AT', '@')
        expected_contents = self.prep(
            '''
            #AT+others
            #AT+node:<GNX>: ** child
            #AT+others
            #AT-others
            #AT-others
        '''
        ).replace('AT', '@')
        test_s = contents.replace('#@', '# @')
        expected = expected_contents.replace('#@', '# @')

        root.b = test_s
        at.initWriteIvars(root)
        at.putBody(root)
        results = ''.join(at.outputList)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestAtFile.test_putBody_unterminated_at_doc_part
    def test_putBody_unterminated_at_doc_part(self):
        at, c = self.at, self.c
        root = c.rootPosition()
        root.h = '@file test.html'

        contents = self.prep(
            '''
    #@@doc
            Unterminated @doc parts (not an error)
        '''
        )

        expected = self.prep(
            '''
            <!--@+doc-->
            <!--
            Unterminated @doc parts (not an error)
            -->
        '''
        )
        root.b = contents
        at.initWriteIvars(root)
        at.putBody(root)
        result = ''.join(at.outputList)
        self.assertEqual(result, expected)

    #@ TestAtFile.test_putCodeLine
    def test_putCodeLine(self):
        at, p = self.at, self.c.p
        at.initWriteIvars(p)
        at.startSentinelComment = '#'
        table = (
            'Line without newline',
            'Line with newline',
            ' ',
        )
        for line in table:
            at.putCodeLine(line, 0)

    #@ TestAtFile.test_putDelims
    def test_putDelims(self):
        at, p = self.at, self.c.p
        at.initWriteIvars(p)
        # Cover the missing code.
        directive = '@delims'
        s = '    @delims <! !>\n'
        at.putDelims(directive, s, 0)

    #@ TestAtFile.test_putLeadInSentinel
    def test_putLeadInSentinel(self):
        at, p = self.at, self.c.p
        at.initWriteIvars(p)
        # Cover the special case code.
        s = '    @others\n'
        at.putLeadInSentinel(s, 0, 2)

    #@ TestAtFile.test_putLine
    def test_putLine(self):
        from leo.core.leoAtFile import LeoIOStatus

        at, p = self.at, self.c.p
        at.initWriteIvars(p)

        # For now, test only the case that hasn't been covered:
        # kind == at.othersDirective and not status.in_code
        status = LeoIOStatus()
        status.in_code = False
        i, kind = 0, at.othersDirective
        s = 'A doc line\n'
        at.putLine(i, kind, p, s, status)

    #@ TestAtFile.test_putRefLine
    def test_putRefLine(self):
        at, p = self.at, self.c.p
        at.initWriteIvars(p)
        # Create one section definition node.
        name1 = g.angleBrackets('section 1')
        child1 = p.insertAsLastChild()
        child1.h = name1
        child1.b = "print('test_putRefLine')\n"
        # Create the valid section reference.
        s = f"  {name1}\n"
        # Careful: init n2 and n2.
        name, n1, n2 = at.findSectionName(s, 0, p)
        self.assertTrue(name)
        at.putRefLine(s, 0, n1, n2, name, p)

    #@ TestAtFile.test_remove
    def test_remove(self):
        at = self.at
        exists = g.os_path_exists

        path = g.os_path_join(g.app.testDir, 'xyzzy')
        if exists(path):
            os.remove(path)  # pragma: no cover

        assert not exists(path)
        assert not at.remove(path)

        f = open(path, 'w')
        f.write('test')
        f.close()

        assert exists(path)
        assert at.remove(path)
        assert not exists(path)

    #@ TestAtFile.test_replaceFile_different_contents
    def test_replaceFile_different_contents(self):
        at = self.at
        encoding = 'utf-8'
        try:
            # https://stackoverflow.com/questions/23212435
            f = tempfile.NamedTemporaryFile(delete=False, encoding=encoding, mode='w')
            fn = f.name
            contents = 'test contents'
            val = at.replaceFile(contents, encoding, fn, self.root_p)
            assert val, val
        finally:
            f.close()
            os.unlink(f.name)

    #@ TestAtFile.test_replaceFile_no_target_file
    def test_replaceFile_no_target_file(self):
        at = self.at
        encoding = 'utf-8'
        at.targetFileName = ''  # The point of this test.
        try:
            # https://stackoverflow.com/questions/23212435
            f = tempfile.NamedTemporaryFile(delete=False, encoding=encoding, mode='w')
            fn = f.name
            contents = 'test contents'
            val = at.replaceFile(contents, encoding, fn, self.root_p)
            assert val, val
        finally:
            f.close()
            os.unlink(f.name)

    #@ TestAtFile.test_replaceFile_same_contents
    def test_replaceFile_same_contents(self):
        at = self.at
        encoding = 'utf-8'
        try:
            # https://stackoverflow.com/questions/23212435
            f = tempfile.NamedTemporaryFile(delete=False, encoding=encoding, mode='w')
            fn = f.name
            contents = 'test contents'
            f.write(contents)
            f.flush()
            val = at.replaceFile(contents, encoding, fn, self.root_p)
            assert not val, val
        finally:
            f.close()
            os.unlink(f.name)

    #@ TestAtFile.test_setPathUa
    def test_setPathUa(self):
        at, p = self.at, self.c.p
        at.setPathUa(p, 'abc')
        d = p.v.tempAttributes
        d2 = d.get('read-path')
        val1 = d2.get('path')
        val2 = at.getPathUa(p)
        table = (
            ('d2.get', val1),
            ('at.getPathUa', val2),
        )
        for kind, val in table:
            self.assertEqual(val, 'abc', msg=kind)

    #@ TestAtFile.test_tabNannyNode
    def test_tabNannyNode(self):
        at, p = self.at, self.c.p

        # Test 1.
        s = self.prep(
            """
            # no error
            def spam():
                pass
        """
        )
        at.tabNannyNode(p, body=s)

        # Test 2.
        s2 = self.prep(
            """
            # syntax error
            def spam:
                pass
              a = 2
        """
        )
        try:
            at.tabNannyNode(p, body=s2)
        except IndentationError:
            pass

    #@ TestAtFile.test_validInAtOthers
    def test_validInAtOthers(self):
        at, p = self.at, self.c.p

        # Just test the last line.
        at.sentinels = False
        at.validInAtOthers(p)

    #@-others


#@< class TestFastAtRead(LeoUnitTest)
class TestFastAtRead(LeoUnitTest):
    """Test the FastAtRead class."""

    def setUp(self):
        super().setUp()
        self.x = leoAtFile.FastAtRead(self.c, gnx2vnode={})

    #@+others
    #@> TestFastAtRead.test_afterref
    def test_afterref(self):
        c, x = self.c, self.x
        h = '@file /test/test_afterLastRef.py'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        #@+<< define expected_body >>
        #@> << define expected_body >>
        # Be careful: no line should look like a Leo sentinel!
        # Use neither a raw string nor an f-string here.
        expected_body = (
            self.prep(
                '''
            ATlanguage python

            a = 1
            if (
            LB test >> ):
                a = 2
        '''
            )
            .replace('AT', '@')
            .replace('LB', '<<')
        )
        #@-<< define expected_body >>
        #@+<< define expected_contents >>
        #@ << define expected_contents >>
        # Be careful: no line should look like a Leo sentinel!
        # Use neither a raw string nor an f-string here.
        expected_contents = (
            self.prep(
                '''
            #AT+leo-ver=5-thin
            #AT+node:{root.gnx}: * {h}
            #AT@language python

            a = 1
            if (
            LB test >> ):
                a = 2
            #AT-leo
        '''
            )
            .replace('AT', '@')
            .replace('LB', '<<')
        )
        expected_contents = expected_contents.replace('{root.gnx}', root.gnx).replace('{h}', root.h)
        #@-<< define expected_contents >>
        test_s = contents.replace('#@', '# @')
        expected = expected_contents.replace('#@', '# @')

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)
        self.assertEqual(root.b, expected_body, msg='mismatch in body')

    #@< TestFastAtRead.test_at_all
    def test_at_all(self):
        c, x = self.c, self.x
        h = '@file /test/test_at_all.txt'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = contents.replace('#@', '# @')
        expected = test_s.replace("# @others doesn't", "#@others doesn't")

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestFastAtRead.test_at_comment (and @first)
    def test_at_comment(self):
        c, x = self.c, self.x
        h = '@file /test/test_at_comment.txt'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = expected = contents

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

        child1 = root.firstChild()
        child2 = child1.next()
        child3 = child2.next()
        table = (
            (child1, g.angleBrackets(' test ')),
            (child2, 'spam'),
            (child3, 'eggs'),
        )
        for child, h in table:
            self.assertEqual(child.h, h)

    #@ TestFastAtRead.test_at_delims
    def test_at_delims(self):
        c, x = self.c, self.x
        h = '@file /test/test_at_delims.txt'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = contents.replace('#@', '# @').replace('!!@', '!! @')
        expected = test_s

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

        child1 = root.firstChild()
        child2 = child1.next()
        child3 = child2.next()
        table = (
            (child1, g.angleBrackets(' test ')),
            (child2, 'spam'),
            (child3, 'eggs'),
        )
        for child, h in table:
            self.assertEqual(child.h, h)

    #@ TestFastAtRead.test_at_last
    def test_at_last(self):
        c, x = self.c, self.x
        h = '@file /test/test_at_last.py'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        #@+<< define expected_body >>
        #@-<< define expected_body >>
        test_s = contents.replace('#@', '# @')
        expected = test_s

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)
        self.assertEqual(root.b, expected_body)

    #@ TestFastAtRead.test_at_others
    def test_at_others(self):
        # In particular, we want to test indented @others.
        c, x = self.c, self.x
        h = '@file /test/test_at_others'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = contents.replace('#@', '# @')
        expected = test_s

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestFastAtRead.test_at_section_delim
    def test_at_section_delim(self):
        # Test the contents of personal test file, slightly altered.

        c, x = self.c, self.x
        h = '@file /test/at_section_delim.py'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = contents.replace('#@', '# @')
        expected = test_s

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

        child1 = root.firstChild()
        child2 = child1.next()
        child3 = child2.next()
        table = (
            (child1, '<!< test >!>'),
            (child2, 'spam'),
            (child3, 'eggs'),
        )
        for child, h in table:
            self.assertEqual(child.h, h)

    #@ TestFastAtRead.test_clones
    def test_clones(self):
        c, x = self.c, self.x
        h = '@file /test/test_clones.py'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = contents.replace('#@', '# @')
        expected = test_s

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)

        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')

        self.assertEqual(results, expected)

        child1 = root.firstChild()
        child2 = child1.next()
        grand_child1 = child1.firstChild()
        grand_child2 = child2.firstChild()
        table = (
            (child1, 'cloned node'),
            (child2, 'cloned node'),
            (grand_child1, 'child'),
            (grand_child2, 'child'),
        )
        for child, h in table:
            self.assertEqual(child.h, h)
        self.assertTrue(child1.isCloned())
        self.assertTrue(child2.isCloned())
        self.assertEqual(child1.v, child2.v)
        self.assertFalse(grand_child1.isCloned())
        self.assertFalse(grand_child2.isCloned())

    #@ TestFastAtRead.test_cweb
    #@@language python

    def test_cweb(self):
        c, x = self.c, self.x
        h = '@file /test/test_cweb.w'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = contents.replace('#@', '# @')
        expected = test_s

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestFastAtRead.test_doc_parts
    def test_doc_parts(self):
        c, x = self.c, self.x
        h = '@file /test/test_directives.py'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        test_s = contents.replace('#@', '# @')
        expected = test_s

        x.read_into_root(test_s, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestFastAtRead.test_doc_parts_html
    def test_doc_parts_html(self):
        c, x = self.c, self.x
        h = '@file /test/test_directives.html'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        #@+<< define expected_contents >>
        #@-<< define expected_contents >>
        test_s = contents
        expected = expected_contents

        x.read_into_root(test_s, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestFastAtRead.test_html_doc_part
    def test_html_doc_part(self):
        c, x = self.c, self.x
        h = '@file /test/test_html_doc_part.html'
        root = c.rootPosition()
        root.h = h  # To match contents.

        #@+<< define contents >>
        #@-<< define contents >>
        #@+<< define expected >>
        #@-<< define expected >>
        test_s = contents.replace('#@', '# @')
        expected = expected.replace('#@', '# @')

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

        x.read_into_root(contents, path='test', root=root)
        s = c.atFileCommands.atFileToString(root, sentinels=True)
        self.assertEqual(s, expected)

    #@ TestFastAtRead.test_minimal_cweb
    #@@language python

    def test_minimal_cweb(self):
        c, x = self.c, self.x
        h = '@file /test/test_cweb.w'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        expected = test_s = contents.replace('#@', '# @')

        x.read_into_root(contents, path='test', root=root)
        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestFastAtRead.test_verbatim
    def test_verbatim(self):
        c, x = self.c, self.x
        h = '@file /test/test_verbatim.py'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        #@+<< define expected_body >>
        #@-<< define expected_body >>
        test_s = expected = contents
        expected = test_s.replace('#@', '# @')
        # Protect the @verbatim line.
        expected = expected.replace('# @+node (verbatim)', '#@+node (verbatim)')

        x.read_into_root(test_s, path='test', root=root)
        if root.b != expected_body:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(root.b), tag='root.b')
            g.printObj(g.splitLines(expected_body), tag='expected_body')
        self.assertEqual(root.b, expected_body)

        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@ TestFastAtRead.test_verbatim_html
    def test_verbatim_html(self):
        c, x = self.c, self.x
        h = '@file /test/test_verbatim.html'
        root = c.rootPosition()
        root.h = h  # To match contents.
        #@+<< define contents >>
        #@-<< define contents >>
        #@+<< define expected_body >>
        #@-<< define expected_body >>

        test_s = contents
        expected = test_s.replace('#@', '# @')
        # Protect the @verbatim line.
        expected = expected.replace('<!-- @+node (verbatim)', '<!--@+node (verbatim)')

        x.read_into_root(test_s, path='test', root=root)
        if root.b != expected_body:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(root.b), tag='root.b')
            g.printObj(g.splitLines(expected_body), tag='expected_body')
        self.assertEqual(root.b, expected_body)

        results = c.atFileCommands.atFileToString(root, sentinels=True)
        if results != expected:
            g.printObj(g.splitLines(test_s), tag='test_s')
            g.printObj(g.splitLines(results), tag='results')
            g.printObj(g.splitLines(expected), tag='expected')
        self.assertEqual(results, expected)

    #@-others


#@-others
#@-leo
