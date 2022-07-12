using EnvDTE;
using System.Windows.Controls;
private void ShowToolWindow(object sender, EventArgs e)
{
    ToolWindowPane window = this.package.FindToolWindow(typeof(ProjectPropertiesToolWindow), 0, true);
    if ((null == window) || (null == window.Frame))
    {
        throw new NotSupportedException("Cannot create window.");
    }
    IVsWindowFrame windowFrame = (IVsWindowFrame)window.Frame;
    Microsoft.VisualStudio.ErrorHandler.ThrowOnFailure(windowFrame.Show());

    // Get the tree view and populate it if there is a project open.
    ProjectPropertiesToolWindowControl control = (ProjectPropertiesToolWindowControl)window.Content;
    TreeView treeView = control.treeView;

    // Reset the TreeView to 0 items.
    treeView.Items.Clear();

    DTE dte = (DTE)this.ServiceProvider.GetService(typeof(DTE));
    Projects projects = dte.Solution.Projects;
    if (projects.Count == 0)   // no project is open
    {
        TreeViewItem item = new TreeViewItem();
        item.Name = "Projects";
        item.ItemsSource = new string[]{ "no projects are open." };
        item.IsExpanded = true;
        treeView.Items.Add(item);
        return;
    }

    Project project = projects.Item(1);
    TreeViewItem item1 = new TreeViewItem();
    item1.Header = project.Name + "Properties";
    treeView.Items.Add(item1);

    foreach (Property property in project.Properties)
    {
        TreeViewItem item = new TreeViewItem();
        item.ItemsSource = new string[] { property.Name };
        item.IsExpanded = true;
        treeView.Items.Add(item);
    }
}