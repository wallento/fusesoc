.. FuseSoC documentation master file, created by
   sphinx-quickstart on Sun Mar 27 16:41:08 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FuseSoC!
===================

FuseSoC is a package manager and a set of build tools for HDL
(Hardware Description Language) code.

Its main purpose is to increase reuse of IP (Intellectual Property)
cores and be an aid for creating, building and simulating SoC
solutions.

The package manager part can be seen as an apt, portage, yum, dnf,
pacman for FPGA (Field-Programmable Gate Array)/ASIC
(Application-Specific Integrated Circuit) IP cores. A simple ini file
describes mainly which files the IP core contains, which other IP
cores it depends on and where FuseSoC shall fetch the code.

A collection of cores together with a top-level is called a system,
and systems can be simulated or passed through the FPGA vendor tools
to build a loadable FPGA image.

Currently FuseSoc supports simulations with ModelSim, Icarus Verilog,
Verilator, Isim and Xsim. It also supports building FPGA images with
Xilinx ISE, Xilinx Vivado and Altera Quartus.

FuseSoC itself does not contain any actual hardware cores, but instead
is configured to look them up in your filesystem.

The main documentation for users is found in the :ref:`user-docs`. If
you are a developer of a hardware core or a system-on-chip, the
:ref:`core-docs` are your starting point.

.. _user-docs:

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   user/installation
   user/configuration

.. _core-docs:

.. toctree::
   :maxdepth: 3
   :caption: Core Documentation

   core/introduction
   core/corefile
   core/backends

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

