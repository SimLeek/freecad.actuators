import subprocess
import functools
import os
import sys


def run_in_freecad(test_func):
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        # Project directory (relative to this file)
        project_dir = os.path.join(os.path.dirname(__file__), '..', '..')

        # Path to the test script we'll generate
        test_script = os.path.join(project_dir, "tests", "temp_test.py")

        # Get the test function's code
        import inspect
        test_code = inspect.getsource(test_func).split("\n")[1:]  # Skip decorator line
        test_code = "\n".join(line[:] for line in test_code)

        # Write a temporary script to run the test
        with open(test_script, "w") as f:
            f.write("import FreeCAD\n")
            f.write("import FreeCADGui\n")
            f.write("import pytest\n")
            f.write(test_code)  # The test function
            f.write("FreeCADGui.showMainWindow()\n")  # Ensure GUI is visible
            f.write(f"\n\n{test_func.__name__}()\n")  # Call the test
            # Keep GUI open: use exec_loop or wait for user input
            f.write("print('Test complete. Press Ctrl+C to close FreeCAD.')\n")
            f.write("FreeCADGui.exec_loop()\n")  # Runs Qt event loop, keeps GUI open
            # No sys.exit(0) to avoid immediate closure

        # Run FreeCAD with -P and -c
        cmd = [
            "freecad",
            "-P", project_dir,
            "-c", f"exec(open('{test_script}').read())"
        ]

        # Run the command, capture output
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True  # Raise CalledProcessError on non-zero exit
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FreeCAD test failed: {e.stderr}")

        # Don’t return result (avoids TypeError in unittest)
        # Test assertions (e.g., pytest.approx) handle pass/fail

    return wrapper


def show_feature_python(obj, doc, solid):
    """
    Set up a FeaturePython object with dummy proxy and view provider, recompute the document,
    and adjust the GUI view to show the object.

    Args:
        obj: FreeCAD object (e.g., Part::FeaturePython)
        doc: FreeCAD document containing the object
    """
    import FreeCAD
    import FreeCADGui
    from freecad import app as App

    class DummyProxy:
        def __init__(self, obj):
            obj.Proxy = self

        def execute(self, fp):
            # Shape is set by the test before calling show_feature_python
            if hasattr(fp, 'Shape') and fp.Shape:
                fp.Shape = solid
            else:
                raise RuntimeError("No valid shape assigned to FeaturePython object")

    class DummyView:
        def __init__(self, vobj):
            vobj.Proxy = self

        def attach(self, vobj):
            self.vobj = vobj

    # Set up proxies
    DummyProxy(obj)
    DummyView(obj.ViewObject)

    # Recompute document
    doc.recompute([obj])

    # Ensure document is active and adjust view
    FreeCAD.setActiveDocument(doc.Name)
    FreeCADGui.ActiveDocument.ActiveView.fitAll()
